from flask import Blueprint, request, jsonify, render_template
from controllers import encryptPwd
from database import registerUser

register = Blueprint('register', __name__, template_folder='templates', url_prefix='/register')


@register.get('/')
def registerGet():
    return render_template("register.html")


@register.post('/')
def registerPost():
    username = str(request.form['username'])
    password = str(request.form['password'])
    if registerUser(username, password):
        return render_template('login.html')
    else:
        return jsonify({'message': 'Error singin up'})
