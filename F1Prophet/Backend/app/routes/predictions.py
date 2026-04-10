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

