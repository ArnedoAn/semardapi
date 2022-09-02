# app.py
from flask import Flask, request, jsonify, render_template, session, make_response
import jwt
import psycopg2
import bcrypt
from functools import wraps
from .views import *


app = Flask(__name__)
app.register_blueprint(login)
app.register_blueprint(data)
app.register_blueprint(register)

app.config['SECRET_KEY'] = '5d3eb228512b0cf7810acdc26397c307'
salt = bcrypt.gensalt()
connection = psycopg2.connect(
    host='semard.postgres.database.azure.com',
    user='andres',
    password='!sem3rd123',
    database='postgres'
)

cursor = connection.cursor()


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request/args.get('token')
        if not token:
            return jsonify({"message": "Token in missing"})
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({"message": "Invalid token"})
    return decorated


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = str(request.form['username'])
#         password = str(request.form['password'])  # hola
#         bpassword = password.encode('utf-8')  # b'hola'
#         hash = str(bcrypt.hashpw(bpassword, salt))
#         try:
#             cursor.callproc('public."REGISTER"', (username, hash))
#             connection.commit()
#             return render_template('login.html')
#         except Exception as ex:
#             connection.rollback()
#             print(ex)
#             return jsonify({'message': 'Error registering', 'error': ex})
#     else:
#         return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            return 'Logged in currently'
    else:
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

# Private Access
# @app.route('/setdata')
# @token_required
# def insertData():
#     try:
#         jsonData = request.get_json()
#         temperature = str(jsonData["temperature"])
#         humidity = str(jsonData["humidity"])
#         cursor.callproc('public."INSERT"', (temperature, humidity))
#         connection.commit()
#         return jsonify({"message": "Success"})
#     except Exception as ex:
#         connection.rollback()
#         print(ex)
#         return jsonify({"message": "error", "error": ex})

# Private Access


# @app.route('/alldata')
# # @token_required
# def getall():
#     try:
#         cursor.callproc('public."SELECT"')
#         rows = cursor.fetchall()
#         return render_template('template.html', objets=rows)
#     except Exception as ex:
#         connection.rollback()
#         print(ex)
#         return jsonify({"message": "error", "error": ex})


# Public Access
# @app.route('/lastone')
# def getone():
#     try:
#         cursor.callproc('public."SELECT_ONLY"')
#         rows = cursor.fetchall()
#         return render_template('template.html', objets=rows)
#     except Exception as ex:
#         connection.rollback()
#         print(ex)
#         return jsonify({"message": "error", "error": ex})
