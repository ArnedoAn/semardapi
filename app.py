from flask import Flask, request
from flask_pyjwt import AuthManager, require_token
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
auth_manager = AuthManager(app)

from entities.nodo import *
from entities.jwt_auth import *
from entities.user import *
from controllers.login_controller import *

# Configuración de Swagger UI
SWAGGER_URL = '/apidocs'  # URL para acceder a la documentación Swagger
API_URL = '/static/swagger.json'  # URL de la especificación Swagger/OpenAPI

# Creación del blueprint de Swagger UI
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Semard API"  # Nombre de tu API
    }
)

# Registro del blueprint en la aplicación Flask
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route("/")
def hello():
    return "Hello World!"

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

if __name__ == '__main__':
    app.run()