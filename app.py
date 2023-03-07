from flask import Flask, request
from flask_pyjwt import AuthManager, require_token

app = Flask(__name__)
auth_manager = AuthManager(app)

from entities.nodo import *
from entities.jwt_auth import *
from entities.user import *
from controllers.login_controller import *

@app.route('/login', methods=['POST'])
def login_post():
    return login(request.get_json())

@app.route('/test', methods=['POST'])
@require_token()
def test():
    result = tester()
    return result

@app.route('/register', methods=['POST'])
def register_post():
    print(request.get_json())
    return register(request.get_json())