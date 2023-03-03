from entities.user import User
from flask import jsonify
from app import auth_manager

def login(data):
    user = User.from_dict(data)
    result = user.login()
    if result is False:
        return jsonify({'message': 'Invalid credentials'}), 401
    token = auth_manager.auth_token(user.id)
    return jsonify({'token': token}), 200

def register(data):
    user = User.from_dict(data)
    result = user.add_user()
    if result is False:
        return jsonify({'message': 'Error adding user'}), 500
    return jsonify({'message': 'User added successfully'}), 200