from entities.user import User
from database.db_postgresql import DBPostgresql as db
from flask import jsonify
from app import auth_manager


def login(data):
    user = User.from_dict(data)
    result = user.login(data.get('password', None))
    if result is False:
        return jsonify({'message': 'Invalid credentials'}), 401
    token = auth_manager.auth_token(user.name, user.dni)
    # refresh_token = auth_manager.refresh_token(user.name)
    return {
        "auth_token": token.signed,
        # "refresh_token": refresh_token.signed
    }, 200


def register(data):
    user = User.from_dict(data)
    result = user.add_user()
    if result is False:
        return jsonify({'message': 'Error adding user'}), 500
    return jsonify({'message': 'User added successfully'}), 200


def tester():
    result = db.get_instance().querys("SELECT * FROM users")
    return jsonify(result), 200
