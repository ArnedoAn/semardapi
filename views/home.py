from flask import Blueprint, render_template

homeEndP = Blueprint('homeEndP', __name__, template_folder='templates', url_prefix='/home')

@homeEndP.get("/")
def hello():
    return "Hello world"

@homeEndP.get("/test")
def test():
    return "test passed!"    

@homeEndP.get("/ruta")
def home():
    return render_template('index.html',{"nombre":"Andres", "curso":1})
