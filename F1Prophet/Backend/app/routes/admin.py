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
        cursor.execute("""
            SELECT p.id, p.user_id, p.fastest_lap
            FROM predictions p
            WHERE p.race_id = %s
        """, (race_id,))
        
        predictions = cursor.fetchall()
        
        if not predictions:
            return jsonify({'error': 'No predictions found for this race'}), 404
        
        points_calculated = 0
        
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
            
            points_calculated += 1
        
        db.commit()
        
        cursor.execute("""
            UPDATE races
            SET status = 'completed'
            WHERE id = %s
        """, (race_id,))
        
        db.commit()
        
        return jsonify({
            'message': f'Points calculated for {points_calculated} predictions',
            'predictions_processed': points_calculated
        }), 200
        
    except Exception as e:
        db.rollback()
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500
    finally:
        cursor.close()