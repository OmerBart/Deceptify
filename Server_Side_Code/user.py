from flask import Blueprint, jsonify
from db import get_db_connection

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users;")
    users = cursor.fetchall()
    return jsonify(users)
