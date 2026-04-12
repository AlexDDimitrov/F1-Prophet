from flask import Blueprint, request, jsonify, g
from ..database import get_db
from functools import wraps
import jwt
from flask import current_app

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
    cursor = db.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT id, name, location, race_date, deadline, season, round_number, status
            FROM races
            WHERE CURRENT_DATE <= race_date
            ORDER BY race_date ASC
            LIMIT 1
        """)
        
        race = cursor.fetchone()
        
        if not race:
            return jsonify({'error': 'No upcoming races'}), 404
        
        return jsonify(race), 200
        
    except Exception as e:
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500
    finally:
        cursor.close()

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
    cursor = db.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT id, deadline, status
            FROM races
            WHERE id = %s
        """, (race_id,))
        
        race = cursor.fetchone()
        
        if not race:
            return jsonify({'error': 'Race not found'}), 404
        
        if race['status'] == 'completed':
            return jsonify({'error': 'Race has already finished'}), 400
        
        from datetime import datetime
        if datetime.now() > race['deadline']:
            return jsonify({'error': 'Prediction deadline has passed'}), 400
        
        cursor.execute("""
            SELECT id FROM predictions
            WHERE user_id = %s AND race_id = %s
        """, (user_id, race_id))
        
        existing = cursor.fetchone()
        
        if existing:
            prediction_id = existing['id']
            
            cursor.execute("""
                UPDATE predictions
                SET fastest_lap = %s, submitted_at = NOW()
                WHERE id = %s
            """, (fastest_lap, prediction_id))
            
            cursor.execute("""
                DELETE FROM predicted_positions
                WHERE prediction_id = %s
            """, (prediction_id,))
            
        else:
            cursor.execute("""
                INSERT INTO predictions (user_id, race_id, fastest_lap)
                VALUES (%s, %s, %s)
            """, (user_id, race_id, fastest_lap))
            
            prediction_id = cursor.lastrowid
        
        for pos in positions:
            cursor.execute("""
                INSERT INTO predicted_positions (prediction_id, driver_id, position, is_dnf)
                VALUES (%s, %s, %s, %s)
            """, (
                prediction_id,
                pos['driver_id'],
                pos.get('position'),
                pos.get('is_dnf', False)
            ))
        
        db.commit()
        
        return jsonify({
            'message': 'Prediction submitted successfully',
            'prediction_id': prediction_id
        }), 201
        
    except Exception as e:
        db.rollback()
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500
    finally:
        cursor.close()

@bp.route('/predictions/my', methods=['GET'])
@token_required
def get_all_my_predictions():
    user_id = g.user_id
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT p.id, p.race_id, p.fastest_lap, p.submitted_at, p.points_earned,
                   r.name as race_name, r.location, r.race_date, r.status
            FROM predictions p
            JOIN races r ON p.race_id = r.id
            WHERE p.user_id = %s
            ORDER BY r.race_date DESC
        """, (user_id,))
        
        predictions = cursor.fetchall()
        
        for prediction in predictions:
            cursor.execute("""
                SELECT driver_id, position, is_dnf
                FROM predicted_positions
                WHERE prediction_id = %s
                ORDER BY position ASC, is_dnf ASC
            """, (prediction['id'],))
            
            prediction['positions'] = cursor.fetchall()
        
        return jsonify(predictions), 200
        
    except Exception as e:
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500
    finally:
        cursor.close()