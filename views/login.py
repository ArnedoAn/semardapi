from flask import Blueprint, request, render_template, session
from database.dbController import *

loginEndP = Blueprint('loginEndP', __name__, template_folder='templates', url_prefix='/login')

@loginEndP.get('/')
def loginGet():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'Logged in currently'


@loginEndP.post('/')
def loginPost():
    username = str(request.form['username'])
    password = str(request.form['password'])
    loginUser(username,password)
    
