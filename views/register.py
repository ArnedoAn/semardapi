from flask import Blueprint, request, jsonify, render_template
from database.dbController import registerUser

registerEndP = Blueprint('registerEndP', __name__, template_folder='templates', url_prefix='/register')


@registerEndP.get('/')
def registerGet():
    return render_template("register.html")


@registerEndP.post('/')
def registerPost():
    username = str(request.form['username'])
    password = str(request.form['password'])
    if registerUser(username, password):
        return render_template('login.html')
    else:
        return jsonify({'message': 'Error singin up'})
