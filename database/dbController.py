import psycopg2
import os
from controllers.pwdController import encryptPwd, validatePwd
from flask import jsonify, session, request
import jwt

key = os.environ.get('SECRET_KEY')

connection = psycopg2.connect(
    host=os.environ.get('DB_HOST'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PWD'),
    database=os.environ.get('DB_DB')
)

cursor = connection.cursor()


def helloW():
    return "Hello World"


def registerUser(username, pwd):
    pwdb = pwd.encode('utf8')
    hash = encryptPwd(pwdb)
    try:
        cursor.callproc('public."REGISTER"', (username, hash))
        connection.commit()
        return True
    except Exception as ex:
        connection.rollback()
        print(ex)
        return False


def loginUser(username, password):
    try:
        cursor.callproc('public."LOGIN"', (username,))
        row = cursor.fetchone()
        print(row)
        if row is None:
            print(row)
            return [False, "Usuario no existe"]
        else:
            pwdHash = row[0]
            if validatePwd(password, pwdHash):
                session['logged_in'] = True
                token = jwt.encode({
                    'user': username,
                    'password': pwdHash
                }, key)
                return [True, token.decode('utf-8')]
            else:
                return [False, "Invalid user o password"]
    except Exception as ex:
        connection.rollback()
        print(ex)
        return [False, ex]


def getLastOne():
    try:
        cursor.callproc('public."SELECT_ONLY"')
        rows = cursor.fetchall()
        return jsonify(rows)
    except Exception as ex:
        connection.rollback()
        print(ex)
        return jsonify({"message": "error", "error": ex})


def getAllData():
    try:
        cursor.callproc('public."SELECT"')
        rows = cursor.fetchall()
        return jsonify(rows)
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
