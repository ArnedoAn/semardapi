from flask import Flask, request
from flask_pyjwt import AuthManager, require_token
from flasgger import Swagger, swag_from

app = Flask(__name__)
auth_manager = AuthManager(app)
# set "/" endpoint on swagger

swagger = Swagger(app, template_file='index.yml')

from entities.nodo import *
from entities.jwt_auth import *
from entities.user import *
from controllers.login_controller import *

@app.route('/')
@swag_from('/index.yml')
def index():
    return "hello world"

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