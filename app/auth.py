from flask import Blueprint, request, jsonify, current_app
from . import mongo # Keep this for the extension instance
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # 1. Access the DB via the app context to prevent NoneType error
    db = mongo.db 

    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Missing email or password"}), 400

    # 2. Check if user exists
    if db.users.find_one({"email": data['email']}):
        return jsonify({"error": "User already exists"}), 409

    hashed_password = generate_password_hash(data['password'])
    
    db.users.insert_one({
        "email": data['email'],
        "password": hashed_password,
        "created_at": datetime.utcnow()
    })
    
    return jsonify({"msg": "User created"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    db = mongo.db # Access DB here too
    
    user = db.users.find_one({"email": data.get('email')})
    
    if user and check_password_hash(user['password'], data.get('password')):
        access_token = create_access_token(identity=str(user['_id']))
        return jsonify(access_token=access_token), 200
    
    return jsonify({"msg": "Invalid credentials"}), 401