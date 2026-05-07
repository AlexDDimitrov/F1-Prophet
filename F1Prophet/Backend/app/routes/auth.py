from flask import Blueprint, request, jsonify, current_app
import bcrypt
from ..database import get_db
from ..models import User
import jwt
from datetime import datetime, timedelta
from .. import limiter

auth_bp = Blueprint('auth', __name__)

def create_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

@auth_bp.route('/register', methods=['POST'])
@limiter.limit("5 per minute")
def register():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON body'}), 400
    
    username = (data.get('username') or '').strip()
    email = (data.get('email') or '').strip().lower()
    password = (data.get('password') or '').strip()

    if not username or not email or not password:
        return jsonify({'error': 'Username, email and password are required'}), 400
    
    if len(username) < 3:
        return jsonify({'error': 'Username must be at least 3 characters long'}), 400
    
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters long'}), 400
    
    db = get_db()

    try:
        existing = db.query(User).filter(
            (User.email == email) | (User.username == username)
        ).first()
        
        if existing:
            return jsonify({'error': 'Email or username already taken'}), 409
        
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        user = User(
            username=username,
            email=email,
            password_hash=hashed.decode('utf-8')
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)

        token = create_token(user.id)

        return jsonify({
            'message': 'Registration successful',
            'token': token,
            'user': {'id': user.id, 'username': user.username, 'email': user.email}
        }), 201

    except Exception as e:
        db.rollback()
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON body'}), 400
 
    email = (data.get('email') or '').strip().lower()
    password = (data.get('password') or '')
 
    if not email or not password:
        return jsonify({'error': 'email and password are required'}), 400
 
    db = get_db()
 
    try:
        user = db.query(User).filter(User.email == email).first()
 
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
 
        password_matches = bcrypt.checkpw(
            password.encode('utf-8'),
            user.password_hash.encode('utf-8')
        )
 
        if not password_matches:
            return jsonify({'error': 'Invalid email or password'}), 401
 
        token = create_token(user.id)
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
        }), 200
 
    except Exception as e:
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    token = request.headers.get('Authorization')
    
    if not token:
        return jsonify({'error': 'Token is missing'}), 401
    
    try:
        if token.startswith('Bearer '):
            token = token[7:]
        
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = data['user_id']
        
        db = get_db()
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_admin': user.is_admin,
            'created_at': user.created_at.isoformat()
        }), 200
        
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401