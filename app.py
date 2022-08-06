#app.py
from flask import Flask,request,jsonify,render_template
import psycopg2
import json

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

app = Flask(__name__)

connection = psycopg2.connect(
    host='semard.postgres.database.azure.com',
    user='andres',
    password='!sem3rd123',
    database='postgres'
)

cursor = connection.cursor()

@app.post('/')
def insertData():
    try:
        jsonData = request.get_json()
        print(jsonData)
        jsonData.toJSON()
        temperature = str(jsonData["temperature"])
        humitity = str(jsonData["humitity"])
        #cursor.execute('CALL INSERT(%s,%s);',(temperature,humitity,))
        cursor.callproc('public."INSERT"',(temperature,humitity))
        connection.commit()
        return jsonify({"message":"Success"})
    except Exception as ex:
        connection.rollback()
        print(ex)
        return jsonify({"message":"error", "error":ex})


@app.get('/')
def getall():
    try:
        cursor.callproc('public."SELECT"')
        rows = cursor.fetchall()
        return render_template('template.html', objets=rows)
    except Exception as ex:
        connection.rollback()
        print(ex)
        return jsonify({"message":"error", "error":ex})

@app.get('/lastone')
def getone():
    try:
        cursor.callproc('public."SELECT_ONLY"')
        rows = cursor.fetchall()
        return render_template('template.html', objets=rows)
    except Exception as ex:
        connection.rollback()
        print(ex)
        return jsonify({"message":"error", "error":ex})
