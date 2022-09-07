from flask import Blueprint

homeEndP = Blueprint('homeEndP', __name__, template_folder='templates', url_prefix='/home')

@homeEndP.get("/")
def hello():
    return "Hello world"

@homeEndP.get("/test")
def test():
    return "test passed!"    