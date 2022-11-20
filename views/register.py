from flask import Blueprint, request, jsonify
from database.dbController import registerUser

registerEndP = Blueprint('registerEndP', __name__, template_folder='templates')


@registerEndP.get('/register')
def registerGet():
    return 'test'


@registerEndP.post("/register")
def registerPost():
    jsonData = request.get_json()
    username = str(jsonData['username'])
    password = str(jsonData['password'])
    if registerUser(username, password):
        return jsonify({'message':'Signed up'})
    else:
        return jsonify({'message': 'Error singin up'})
