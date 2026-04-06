from flask import Blueprint, request, jsonify
import bcrypt
from ..database import get_db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json(silent = True)
    if not data:
        return jsonify({
            'error': 'Invalid JSON body'
        }), 400
    
    username = data.get('username' or '').strip()
    email    = (data.get('email')    or '').strip().lower()
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

        return jsonify({
            'message': 'Registration successful',
            'user': {'id': user_id, 'username': username, 'email': email}
        }), 201

    except Exception as e:
        db.rollback()
        return jsonify({
            'error': 'Server error', 'detail': str(e)
            }), 500
    
    finally:
        cursor.close()
