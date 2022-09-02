from flask import Blueprint, request, jsonify, render_template, session, make_response
import psycopg2
import jwt
import bcrypt

login = Blueprint('login', __name__, template_folder='templates', url_prefix='/login')

salt = bcrypt.gensalt()
connection = psycopg2.connect(
    host='semard.postgres.database.azure.com',
    user='andres',
    password='!sem3rd123',
    database='postgres'
)

cursor = connection.cursor()


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
    try:
        cursor.callproc('public."LOGIN"', (username,))
        row = cursor.fetchone()
        print(row)
        if row is None:
            print(row)
            return "Usuario no existe"
        else:
            pwdHash = row[0]
            if bcrypt.checkpw(password, pwdHash):
                session['logged_in'] = True
                token = jwt.encode({
                    'user': username,
                    'password': pwdHash
                }, app.config['SECRET_KEY'])
                return jsonify({'message': 'Loggen in', 'token': token.decode('utf-8')})
            else:
                return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Authentication Failed'})
    except Exception as ex:
        connection.rollback()
        print(ex)
        return jsonify({'message': 'Error registering', 'error': ex})
