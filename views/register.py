from flask import Blueprint,request, jsonify, render_template
import psycopg2
import bcrypt

register = Blueprint('register', __name__, template_folder='templates', url_prefix='/register')
salt = bcrypt.gensalt()

connection = psycopg2.connect(
    host='semard.postgres.database.azure.com',
    user='andres',
    password='!sem3rd123',
    database='postgres'
)

cursor = connection.cursor()

@register.get('/')
def registerGet():
    return render_template("register.html")

@register.post('/')
def registerPost():
    username = str(request.form['username'])
    password = str(request.form['password'])  # hola
    bpassword = password.encode('utf-8')  # b'hola'
    hash = str(bcrypt.hashpw(bpassword, salt))
    try:
        cursor.callproc('public."REGISTER"', (username, hash))
        connection.commit()
        return render_template('login.html')
    except Exception as ex:
        connection.rollback()
        print(ex)
        return jsonify({'message': 'Error registering', 'error': ex})