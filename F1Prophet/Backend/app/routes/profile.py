from flask import Blueprint, jsonify, g
from ..database import get_db
from ..models import User, Prediction, Race
from sqlalchemy import func, desc
from functools import wraps
import jwt
from flask import current_app, request

bp = Blueprint('profile', __name__, url_prefix='/api/users')

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

@bp.route('/profile', methods=['GET'])
@token_required
def get_profile():
    db = get_db()
    user_id = g.user_id
    
    try:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        total_predictions = db.query(func.count(Prediction.id)).filter(
            Prediction.user_id == user_id
        ).scalar()
        
        all_time_rank_query = db.query(
            func.count(func.distinct(User.id))
        ).filter(
            User.total_points > user.total_points
        ).scalar()
        
        global_rank = (all_time_rank_query or 0) + 1
        
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'total_points': user.total_points,
            'created_at': user.created_at.isoformat(),
            'predictions_made': total_predictions,
            'global_rank': global_rank
        }), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500

@bp.route('/stats', methods=['GET'])
@token_required
def get_stats():
    db = get_db()
    user_id = g.user_id
    
    try:
        predictions_with_points = db.query(Prediction).join(
            Race
        ).filter(
            Prediction.user_id == user_id,
            Prediction.points_earned.isnot(None)
        ).all()
        
        if not predictions_with_points:
            return jsonify({
                'best_prediction': None,
                'average_points': 0,
                'total_completed': 0
            }), 200
        
        best_prediction = max(predictions_with_points, key=lambda p: p.points_earned)
        
        race_info = db.query(Race).filter(Race.id == best_prediction.race_id).first()
        
        total_points = sum(p.points_earned for p in predictions_with_points)
        average_points = total_points / len(predictions_with_points)
        
        return jsonify({
            'best_prediction': {
                'points': best_prediction.points_earned,
                'race_name': race_info.name if race_info else 'Unknown',
                'race_location': race_info.location if race_info else 'Unknown',
                'race_date': race_info.race_date.isoformat() if race_info else None
            },
            'average_points': round(average_points, 2),
            'total_completed': len(predictions_with_points),
        }), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500