from flask import Blueprint, request, jsonify, g
from ..database import get_db
from ..services.points_service import PointsCalculationService
from functools import wraps
import jwt
from flask import current_app

bp = Blueprint('admin', __name__, url_prefix='/api/admin')

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = data['user_id']
            
            db = get_db()
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT is_admin FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            cursor.close()
            
            if not user or not user['is_admin']:
                return jsonify({'error': 'Admin access required'}), 403
            
            g.user_id = user_id
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

@bp.route('/calculate-points/<int:race_id>', methods=['POST'])
@admin_required
def calculate_race_points(race_id):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON body'}), 400
    
    actual_results = data.get('actual_results', [])
    actual_fastest_lap = data.get('fastest_lap')
    
    if not actual_results:
        return jsonify({'error': 'actual_results is required'}), 400
    
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    try:
        cursor.execute("DELETE FROM race_results WHERE race_id = %s", (race_id,))

        for result in actual_results:
            is_fastest_lap = 1 if result['driver_id'] == actual_fastest_lap else 0
            
            cursor.execute("""
                INSERT INTO race_results (race_id, driver_id, position, is_dnf, fastest_lap)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                race_id,
                result['driver_id'],
                result.get('position'),
                result.get('is_dnf', False),
                is_fastest_lap
            ))
        
        db.commit()

        cursor.execute("""
            SELECT p.id, p.user_id, p.fastest_lap
            FROM predictions p
            WHERE p.race_id = %s
        """, (race_id,))
        
        predictions = cursor.fetchall()
        
        if not predictions:
            return jsonify({'error': 'No predictions found for this race'}), 404
        
        points_calculated = 0
        user_points_updates = {}
        
        for prediction in predictions:
            cursor.execute("""
                SELECT driver_id, position, is_dnf
                FROM predicted_positions
                WHERE prediction_id = %s
            """, (prediction['id'],))
            
            predicted_positions = cursor.fetchall()
            
            points_breakdown = PointsCalculationService.calculate_points(
                predicted_positions=predicted_positions,
                actual_results=actual_results,
                predicted_fastest_lap=prediction['fastest_lap'],
                actual_fastest_lap=actual_fastest_lap
            )
            
            cursor.execute("""
                UPDATE predictions
                SET points_earned = %s
                WHERE id = %s
            """, (points_breakdown['total_points'], prediction['id']))
            
            user_id = prediction['user_id']
            if user_id not in user_points_updates:
                user_points_updates[user_id] = 0
            user_points_updates[user_id] += points_breakdown['total_points']
            
            points_calculated += 1
        
        db.commit()
    
        for user_id, points_earned in user_points_updates.items():
            cursor.execute("""
                UPDATE users
                SET total_points = total_points + %s
                WHERE id = %s
            """, (points_earned, user_id))
        
        db.commit()
        
        cursor.execute("""
            UPDATE races
            SET status = 'completed'
            WHERE id = %s
        """, (race_id,))
        
        db.commit()
        
        return jsonify({
            'message': f'Points calculated for {points_calculated} predictions',
            'predictions_processed': points_calculated,
            'users_updated': len(user_points_updates)
        }), 200
        
    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500
    finally:
        cursor.close()


@bp.route('/race-results/<int:race_id>', methods=['GET'])
def get_race_results(race_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT driver_id, position, is_dnf, fastest_lap
            FROM race_results
            WHERE race_id = %s
            ORDER BY 
                CASE WHEN is_dnf = 1 THEN 999 ELSE position END ASC
        """, (race_id,))
        
        results = cursor.fetchall()

        fastest_lap_driver = None
        for result in results:
            if result['fastest_lap']:
                fastest_lap_driver = result['driver_id']
                break
        
        return jsonify({
            'race_id': race_id,
            'results': results,
            'fastest_lap': fastest_lap_driver
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500
    finally:
        cursor.close()