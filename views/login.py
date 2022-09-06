from flask import Blueprint, request, render_template
from database import *

login = Blueprint('login', __name__, template_folder='templates', url_prefix='/login')

@login.get('/')
def loginGet():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'Logged in currently'


@login.post('/')
def loginPost():
    username = str(request.form['username'])
    password = str(request.form['password'])
    loginUser(username,password)
    
