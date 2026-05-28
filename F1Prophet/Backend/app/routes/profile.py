from flask import Blueprint, jsonify, g
from ..database import get_db
from ..models import User, Prediction, Race
from sqlalchemy import func
import bcrypt
from flask import request
from ..middleware.auth_guard import token_required

bp = Blueprint('profile', __name__, url_prefix='/api/users')

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
        
        favorite_driver = 'None'
        favorite_team = 'None'

        driver_map = {
            "max_verstappen": "Max Verstappen",
            "antonelli": "Kimi Antonelli",
            "russell": "George Russell",
            "leclerc": "Charles Leclerc",
            "norris": "Lando Norris",
            "hamilton": "Lewis Hamilton",
            "piastri": "Oscar Piastri",
            "colapinto": "Franco Colapinto",
            "hadjar": "Isack Hadjar",
            "sainz": "Carlos Sainz",
            "albon": "Alex Albon",
            "gasly": "Pierre Gasly",
            "bortoleto": "Gabriel Bortoleto",
            "bearman": "Oliver Bearman",
            "ocon": "Esteban Ocon",
            "lawson": "Liam Lawson",
            "arvid_lindblad": "Arvid Lindblad",
            "alonso": "Fernando Alonso",
            "stroll": "Lance Stroll",
            "hulkenberg": "Nico Hülkenberg",
            "perez": "Sergio Pérez",
            "bottas": "Valtteri Bottas",
        }

        if user.favorite_driver in driver_map:
            favorite_driver = driver_map[user.favorite_driver]
            
        team_map = {
            "alpine": "Alpine F1 Team",
            "aston_martin": "Aston Martin",
            "audi": "Audi",
            "cadillac": "Cadillac F1 Team",
            "ferrari": "Ferrari",
            "haas": "Haas F1 Team",
            "mclaren": "McLaren",
            "mercedes": "Mercedes",
            "rb": "RB F1 Team",
            "red_bull": "Red Bull",
            "williams": "Williams",
        }

        if user.favorite_team in team_map:
            favorite_team = team_map[user.favorite_team]

        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'total_points': user.total_points,
            'created_at': user.created_at.isoformat(),
            'predictions_made': total_predictions,
            'global_rank': global_rank,
            'favorite_driver': favorite_driver,
            'favorite_team': favorite_team
        }), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500
    
@bp.route('/profile', methods=['PUT'])
@token_required
def update_profile():
    db = get_db()
    user_id = g.user_id
    
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON body'}), 400
    
    try:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        current_password = data.get('current_password', '').strip()
        new_password = data.get('new_password', '').strip()
        
        if username and username != user.username:
            if len(username) < 3:
                return jsonify({'error': 'Username must be at least 3 characters long'}), 400
            
            existing_user = db.query(User).filter(
                User.username == username,
                User.id != user_id
            ).first()
            
            if existing_user:
                return jsonify({'error': 'Username already taken'}), 409
            
            user.username = username
        
        if email and email != user.email:
            existing_user = db.query(User).filter(
                User.email == email,
                User.id != user_id
            ).first()
            
            if existing_user:
                return jsonify({'error': 'Email already taken'}), 409
            
            user.email = email
        
        if new_password:
            if not current_password:
                return jsonify({'error': 'Current password is required to set new password'}), 400
            
            password_matches = bcrypt.checkpw(
                current_password.encode('utf-8'),
                user.password_hash.encode('utf-8')
            )
            
            if not password_matches:
                return jsonify({'error': 'Current password is incorrect'}), 401
            
            if len(new_password) < 6:
                return jsonify({'error': 'New password must be at least 6 characters long'}), 400
            
            hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            user.password_hash = hashed.decode('utf-8')
        
        db.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }), 200
        
    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500
    
@bp.route('/profile/favorite-driver/<driver_id>', methods = ['POST'])
@token_required
def set_fav_driver(driver_id):
    db = get_db()
    user_id = g.user_id

    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if user.favorite_driver == driver_id:
            user.favorite_driver = None
            db.commit()
            return jsonify({
                'message': 'Favorite driver removed',
                'favorite_driver': None
            }), 200

        user.favorite_driver = driver_id
        db.commit()

        return jsonify({
                'message': 'Favorite driver set successfully',
                'favorite_driver': driver_id
            }), 200
    except Exception as e:
        db.rollback()
        import traceback
        traceback().print_exc()
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500

@bp.route('/profile/favorite-team/<team_id>', methods = ['POST'])
@token_required
def set_fav_team(team_id):
    db = get_db()
    user_id = g.user_id

    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if user.favorite_team == team_id:
            user.favorite_team = None
            db.commit()
            return jsonify({
                'message': 'Favorite team removed',
                'favorite_team': None
            }), 200

        user.favorite_team = team_id
        db.commit()

        return jsonify({
                'message': 'Favorite team set successfully',
                'favorite_team': team_id
            }), 200
    except Exception as e:
        db.rollback()
        import traceback
        traceback().print_exc()
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
            'total_points': total_points
        }), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500