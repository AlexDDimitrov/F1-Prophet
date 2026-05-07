from flask import Blueprint, request, jsonify, g
from ..database import get_db
from ..models import Race, Prediction, PredictedPosition
from functools import wraps
import jwt
from flask import current_app
from datetime import datetime

bp = Blueprint('predictions', __name__, url_prefix='/api')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            g.user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

@bp.route('/races/current', methods=['GET'])
def get_current_race():
    db = get_db()
    
    try:
        race = db.query(Race).filter(
            Race.race_date >= datetime.now()
        ).order_by(Race.race_date.asc()).first()
        
        if not race:
            return jsonify({'error': 'No upcoming races'}), 404
        
        return jsonify({
            'id': race.id,
            'name': race.name,
            'location': race.location,
            'race_date': race.race_date.isoformat(),
            'deadline': race.deadline.isoformat(),
            'season': race.season,
            'round_number': race.round_number,
            'status': race.status
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500

@bp.route('/races/all', methods=['GET'])
def get_all_races():
    db = get_db()
    
    try:
        races = db.query(Race).filter(
            Race.season == 2026
        ).order_by(Race.round_number.asc()).all()
        
        result = []
        for race in races:
            result.append({
                'id': race.id,
                'name': race.name,
                'location': race.location,
                'race_date': race.race_date.isoformat(),
                'deadline': race.deadline.isoformat(),
                'season': race.season,
                'round_number': race.round_number,
                'status': race.status
            })
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500

@bp.route('/predictions', methods=['POST'])
@token_required
def submit_prediction():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON body'}), 400
    
    race_id = data.get('race_id')
    positions = data.get('positions', [])
    fastest_lap = data.get('fastest_lap')
    
    if not race_id or not positions:
        return jsonify({'error': 'race_id and positions are required'}), 400
    
    user_id = g.user_id
    db = get_db()
    
    try:
        race = db.query(Race).filter(Race.id == race_id).first()
        
        if not race:
            return jsonify({'error': 'Race not found'}), 404
        
        if race.status == 'completed':
            return jsonify({'error': 'Race has already finished'}), 400
        
        if datetime.now() > race.deadline:
            return jsonify({'error': 'Prediction deadline has passed'}), 400
        
        existing = db.query(Prediction).filter(
            Prediction.user_id == user_id,
            Prediction.race_id == race_id
        ).first()
        
        if existing:
            existing.fastest_lap = fastest_lap
            existing.submitted_at = datetime.utcnow()
            
            db.query(PredictedPosition).filter(
                PredictedPosition.prediction_id == existing.id
            ).delete()
            
            prediction_id = existing.id
        else:
            prediction = Prediction(
                user_id=user_id,
                race_id=race_id,
                fastest_lap=fastest_lap
            )
            db.add(prediction)
            db.flush()
            prediction_id = prediction.id
        
        for pos in positions:
            predicted_pos = PredictedPosition(
                prediction_id=prediction_id,
                driver_id=pos['driver_id'],
                position=pos.get('position'),
                is_dnf=pos.get('is_dnf', False)
            )
            db.add(predicted_pos)
        
        db.commit()
        
        return jsonify({
            'message': 'Prediction submitted successfully',
            'prediction_id': prediction_id
        }), 201
        
    except Exception as e:
        db.rollback()
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500

@bp.route('/predictions/my', methods=['GET'])
@token_required
def get_all_my_predictions():
    user_id = g.user_id
    db = get_db()
    
    try:
        predictions = db.query(Prediction).join(Race).filter(
            Prediction.user_id == user_id
        ).order_by(Race.race_date.desc()).all()
        
        result = []
        for prediction in predictions:
            positions = []
            for pos in prediction.positions:
                positions.append({
                    'driver_id': pos.driver_id,
                    'position': pos.position,
                    'is_dnf': pos.is_dnf
                })
            
            result.append({
                'id': prediction.id,
                'race_id': prediction.race_id,
                'fastest_lap': prediction.fastest_lap,
                'submitted_at': prediction.submitted_at.isoformat(),
                'points_earned': prediction.points_earned,
                'race_name': prediction.race.name,
                'location': prediction.race.location,
                'race_date': prediction.race.race_date.isoformat(),
                'status': prediction.race.status,
                'positions': positions
            })
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500