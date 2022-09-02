from flask import Blueprint, request, jsonify, render_template
import psycopg2
from functools import wraps

data = Blueprint('data', __name__, template_folder='templates')

connection = psycopg2.connect(
    host='semard.postgres.database.azure.com',
    user='andres',
    password='!sem3rd123',
    database='postgres'
)


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


cursor = connection.cursor()


@data.route('/setdata', methods=['POST'])
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


@data.route('/alldata')
def allData():
    try:
        cursor.callproc('public."SELECT"')
        rows = cursor.fetchall()
        return render_template('template.html', objets=rows)
    except Exception as ex:
        connection.rollback()
        print(ex)
        return jsonify({"message": "error", "error": ex})


@data.route('/lastone')
def lastOne():
    try:
        cursor.callproc('public."SELECT_ONLY"')
        rows = cursor.fetchall()
        return render_template('template.html', objets=rows)
    except Exception as ex:
        connection.rollback()
        print(ex)
        return jsonify({"message": "error", "error": ex})
