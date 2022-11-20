from flask import Blueprint, request, render_template, session
from database.dbController import *

loginEndP = Blueprint('loginEndP', __name__,
                      template_folder='templates', url_prefix='/login')


@loginEndP.get('/login')
def loginGet():
    if not session.get('logged_in'):
        return jsonify({"message": "Logged"})
    else:
        return jsonify({"message": 'Logged in currently'})


@loginEndP.post('')
def loginPost():
    jsonData = request.get_json()
    username = str(jsonData['username'])
    password = str(jsonData['password'])
    try:
        token = loginUser(username, password)
        if token[0] != False:
            return jsonify({'message': "success", 'token': token})
        else:
            return jsonify({'message': 'failed', 'error': token[1]})
    except Exception as ex:
        print(ex)
        return jsonify({'message': "failed", 'error': ex})
