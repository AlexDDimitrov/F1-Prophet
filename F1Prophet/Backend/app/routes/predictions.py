from flask import Blueprint, request, jsonify, g
from ..database import get_db
from ..models import Race, Prediction, PredictedPosition
from datetime import datetime
from ..middleware.auth_guard import token_required

bp = Blueprint('predictions', __name__, url_prefix='/api/predictions')

@bp.route('/', methods=['POST'])
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

@bp.route('/my', methods=['GET'])
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