from flask import request,jsonify
import jwt
from app import app
from functools import wraps

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers['token']
        if not token:
            return jsonify({"message": "Token in missing"})
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({"message": "Invalid token"})
    return decorated