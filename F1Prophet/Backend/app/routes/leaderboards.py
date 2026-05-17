from time import time

from flask import Blueprint, jsonify, g
from ..database import get_db
from ..models import User, Prediction, Race
from sqlalchemy import func, extract
from functools import wraps
import jwt
from flask import current_app, request

bp = Blueprint('leaderboards', __name__, url_prefix='/api/leaderboards')

def token_optional(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if token:
            try:
                if token.startswith('Bearer '):
                    token = token[7:]
                
                data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
                g.user_id = data['user_id']
            except:
                g.user_id = None
        else:
            g.user_id = None
        
        return f(*args, **kwargs)
    
    return decorated

@bp.route('/monthly/<int:year>/<int:month>', methods=['GET'])
@token_optional
def get_monthly_leaderboard(year, month):
    db = get_db()
    
    try:
        leaderboard = db.query(
            User.id,
            User.username,
            func.sum(Prediction.points_earned).label('total_points'),
            func.count(Prediction.id).label('predictions_count')
        ).join(
            Prediction, User.id == Prediction.user_id
        ).join(
            Race, Prediction.race_id == Race.id
        ).filter(
            Race.season == (str(year)),
            extract('month', Race.race_date) == (str(month)),
            (Prediction.points_earned.isnot(None)) | (Prediction.id.is_(None) | (User.id == g.user_id if hasattr(g, 'user_id') else False))
        ).group_by(
            User.id, User.username
        ).order_by(
            func.sum(Prediction.points_earned).desc()
        ).limit(50).all()
        
        result = []
        current_user_rank = None
        
        for index, entry in enumerate(leaderboard, start=1):
            user_data = {
                'rank': index,
                'user_id': entry.id,
                'username': entry.username,
                'total_points': int(entry.total_points) if entry.total_points else 0,
                'predictions_count': entry.predictions_count,
                'is_current_user': entry.id == g.user_id if hasattr(g, 'user_id') else False
            }
            
            result.append(user_data)
            
            if hasattr(g, 'user_id') and entry.id == g.user_id:
                current_user_rank = index

        return jsonify({
            'leaderboard': result,
            'current_user_rank': current_user_rank,
            'year': year,
            'month': month,
            'total_users': len(result)
        }), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500

@bp.route('/seasonal/<int:year>', methods=['GET'])
@token_optional
def get_seasonal_leaderboard(year):
    db = get_db()
    
    try:
        leaderboard = db.query(
            User.id,
            User.username,
            func.sum(Prediction.points_earned).label('total_points'),
            func.count(Prediction.id).label('predictions_count')
        ).join(
            Prediction, User.id == Prediction.user_id
        ).join(
            Race, Prediction.race_id == Race.id
        ).filter(
            Race.season == (str(year)),
            (Prediction.points_earned.isnot(None)) | (Prediction.id.is_(None) | (User.id == g.user_id if hasattr(g, 'user_id') else False))
        ).group_by(
            User.id, User.username
        ).order_by(
            func.sum(Prediction.points_earned).desc()
        ).limit(50).all()
        
        result = []
        current_user_rank = None
        
        for index, entry in enumerate(leaderboard, start=1):
            user_data = {
                'rank': index,
                'user_id': entry.id,
                'username': entry.username,
                'total_points': int(entry.total_points) if entry.total_points else 0,
                'predictions_count': entry.predictions_count,
                'is_current_user': entry.id == g.user_id if hasattr(g, 'user_id') else False
            }
            
            result.append(user_data)
            
            if hasattr(g, 'user_id') and entry.id == g.user_id:
                current_user_rank = index
        
        return jsonify({
            'leaderboard': result,
            'current_user_rank': current_user_rank,
            'year': year,
            'total_users': len(result)
        }), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500

@bp.route('/all-time', methods=['GET'])
@token_optional
def get_alltime_leaderboard():
    db = get_db()
    
    try:
        leaderboard_query = db.query(
            User.id,
            User.username,
            User.total_points,
            func.count(Prediction.id).label('predictions_count')
        ).join(
            Prediction, User.id == Prediction.user_id
        ).filter(
            (Prediction.points_earned.isnot(None)) | (Prediction.id.is_(None) | (User.id == g.user_id if hasattr(g, 'user_id') else False))
        ).group_by(
            User.id, User.username, User.total_points
        )
        
        if hasattr(g, 'user_id') and g.user_id:
            leaderboard_query = leaderboard_query.having(
                (func.count(Prediction.id) > 0) | (User.id == g.user_id)
            )
        else:
            leaderboard_query = leaderboard_query.having(
                func.count(Prediction.id) > 0
            )
        
        leaderboard = leaderboard_query.order_by(
            User.total_points.desc()
        ).limit(50).all()
        
        result = []
        current_user_rank = None
        
        for index, entry in enumerate(leaderboard, start=1):
            if entry.total_points == 0 and entry.predictions_count == 0 and entry.id != g.user_id:
                continue

            user_data = {
                'rank': index,
                'user_id': entry.id,
                'username': entry.username,
                'total_points': entry.total_points,
                'predictions_count': entry.predictions_count,
                'is_current_user': entry.id == g.user_id if hasattr(g, 'user_id') else False
            }
            
            result.append(user_data)
            
            if hasattr(g, 'user_id') and entry.id == g.user_id:
                current_user_rank = index
        
        return jsonify({
            'leaderboard': result,
            'current_user_rank': current_user_rank,
            'total_users': len(result)
        }), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500