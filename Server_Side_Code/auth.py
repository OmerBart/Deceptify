from flask import Blueprint, request, jsonify
from db import get_db_connection
import psycopg2
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if not all(key in data for key in ('username', 'password')):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM users WHERE username = %s;", (data['username'],))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(data['password'].encode('utf-8'), user[1].encode('utf-8')):
            return jsonify({'status': 'Login successful', 'id': user[0]})
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

@auth_bp.route('/data', methods=['POST'])
def create_user():
    data = request.json
    if not all(key in data for key in ('username', 'password')):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s;", (data['username'],))
        if cursor.fetchone() is not None:
            return jsonify({'error': 'Username already exists'}), 409

        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id;", (data['username'], hashed_password))
        user_id = cursor.fetchone()[0]
        conn.commit()
        return jsonify({'status': 'User created successfully', 'id': user_id})
    except Exception as e:
        print(f"Error during user creation: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()
