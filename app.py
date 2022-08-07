# app.py
from flask import Flask, request, jsonify, render_template, session, make_response
import jwt
import psycopg2
import bcrypt
from functools import wraps

app = Flask(__name__)
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




app.get('/register')
def register():
    username = request.form['username']
    password = request.form['password']
    bpassword = password.encode('utf-8')
    hash = bcrypt.hashpw(bpassword, salt)
    try:
        cursor.callproc('public."REGISTER"', (username, hash))
        cursor.commit()
        return render_template('login.html')
    except Exception as ex:
        connection.rollback()
        print(ex)
        return jsonify({'message': 'Error registering', 'error': ex})


app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='GET':
        # if not session.get('logged_in'):
        #     return render_template('login.html')
        # else:
        #     return 'Logged in currently'
        return '<h1>Done<\h1>'
    else:
        username = request.form['username']
        password = request.form['password']
        cursor.callproc('public."LOGIN"', (username,))
        row = cursor.fetchone
        pwdHash = row[1]
        if bcrypt.checkpw(password, pwdHash):
            session['logged_in'] = True
            token = jwt.encode({
                'user': username,
                'password': pwdHash
            }, app.config['SECRET_KEY'])
            return jsonify({'message': 'Loggen in', 'token': token.decode('utf-8')})
        else:
            return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Authentication Failed'})
   


# Private Access
@app.post('/setdata')
#@token_required
def insertData():
    try:
        jsonData = request.get_json()
        temperature = str(jsonData["temperature"])
        humidity = str(jsonData["humidity"])
        cursor.callproc('public."INSERT"', (temperature, humidity))
        connection.commit()
        return jsonify({"message": "Success"})
    except Exception as ex:
        connection.rollback()
        print(ex)
        return jsonify({"message": "error", "error": ex})

# Private Access


@app.get('/alldata')
#@token_required
def getall():
    try:
        cursor.callproc('public."SELECT"')
        rows = cursor.fetchall()
        return render_template('template.html', objets=rows)
    except Exception as ex:
        connection.rollback()
        print(ex)
        return jsonify({"message": "error", "error": ex})

app.get('/a')
def a():
    return 'a'

# Public Access
@app.get('/lastone')
def getone():
    try:
        cursor.callproc('public."SELECT_ONLY"')
        rows = cursor.fetchall()
        return render_template('template.html', objets=rows)
    except Exception as ex:
        connection.rollback()
        print(ex)
        return jsonify({"message": "error", "error": ex})
