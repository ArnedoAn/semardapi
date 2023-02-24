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

@app.router('/test', methods=['POST'])
@require_token()
def test():
    return 'test'