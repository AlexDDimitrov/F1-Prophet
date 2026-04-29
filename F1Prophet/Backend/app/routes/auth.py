from flask import Blueprint, request, jsonify, current_app
import bcrypt
from ..database import get_db
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
    data = request.get_json(silent = True)
    if not data:
        return jsonify({
            'error': 'Invalid JSON body'
        }), 400
    
    username = data.get('username' or '').strip()
    email = (data.get('email')    or '').strip().lower()
    password = (data.get('password') or '').strip()

    if not username or not email or not password:
        return jsonify({
            'error': 'Username, email and password are required'
        }), 400
    
    if len(username) < 3:
        return jsonify({
            'error': 'Username must be at least 3 characters long'
        }), 400
    
    if len(password) < 6:
        return jsonify({
            'error': 'Password must be at least 6 characters long'
        }), 400
    
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            'SELECT id FROM users WHERE email = %s OR username = %s',
            (email, username)
        )
        if cursor.fetchone():
            return jsonify({'error': 'Email or username already taken'}), 409
        
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)',
            (username, email, hashed.decode('utf-8'))
        )
        db.commit()

        user_id = cursor.lastrowid

        token = create_token(user_id)

        return jsonify({
            'message': 'Registration successful',
            'token': token,
            'user': {'id': user_id, 'username': username, 'email': email}
        }), 201

    except Exception as e:
        db.rollback()
        return jsonify({
            'error': 'Server error', 'detail': str(e)
            }), 500
    
    finally:
        cursor.close()

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
    cursor = db.cursor(dictionary=True)
 
    try:
        cursor.execute(
            'SELECT id, username, email, password_hash FROM users WHERE email = %s',
            (email,)
        )
        user = cursor.fetchone()
 
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
 
        password_matches = bcrypt.checkpw(
            password.encode('utf-8'),
            user['password_hash'].encode('utf-8')
        )
 
        if not password_matches:
            return jsonify({'error': 'Invalid email or password'}), 401
 
        token = create_token(user['id'])
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id':       user['id'],
                'username': user['username'],
                'email':    user['email'],
            }
        }), 200
 
    except Exception as e:
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500
 
    finally:
        cursor.close()

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
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT id, username, email, is_admin, created_at
            FROM users
            WHERE id = %s
        """, (user_id,))
        
        user = cursor.fetchone()
        cursor.close()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user), 200
        
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401