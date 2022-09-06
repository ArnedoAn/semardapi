import psycopg2
from controllers import encryptPwd,validatePwd
from flask import jsonify, render_template, session, make_response, request
import jwt
from app import app

connection = psycopg2.connect(
    host='motty.db.elephantsql.com',
    user='wwavtnoi',
    password='!sem3rd123',
    database='postgres'
)

cursor = connection.cursor()

def registerUser(username, pwd):
    pwdb = pwd.encode('utf-8')
    hash = encryptPwd(pwdb)
    try:
        cursor.callproc('public."REGISTER"', (username, hash))
        connection.commit()
        return True
    except Exception as ex:
        connection.rollback()
        print(ex)
        return False

def loginUser(username,password):
    try:
        cursor.callproc('public."LOGIN"', (username,))
        row = cursor.fetchone()
        print(row)
        if row is None:
            print(row)
            return "Usuario no existe"
        else:
            pwdHash = row[0]
            if validatePwd(password, pwdHash):
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

def getLastOne():
    try:
        cursor.callproc('public."SELECT_ONLY"')
        rows = cursor.fetchall()
        return render_template('template.html', objets=rows)
    except Exception as ex:
        connection.rollback()
        print(ex)
        return jsonify({"message": "error", "error": ex})

def getAllData():
    try:
        cursor.callproc('public."SELECT"')
        rows = cursor.fetchall()
        return render_template('template.html', objets=rows)
    except Exception as ex:
        connection.rollback()
        print(ex)
        return jsonify({"message": "error", "error": ex})  

def setData():
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
       