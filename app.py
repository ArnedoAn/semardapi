#app.py
from flask import Flask,request,jsonify
import psycopg2
import json

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
        name = jsonData["name"]
        cursor.execute('insert into public."test"(name) values(%s)',(name,))
        connection.commit()
        return jsonify({"message":"Success"})
    except Exception as ex:
        print(ex)
        return jsonify({"message":"Error"})


@app.get('/')
def hello():
    cursor.execute('select * from "test"')
    rows = cursor.fetchall()
    dic=['id','name']
    aux=[]
    for row in rows:
        aux.append(dict(zip(dic, row)))
    jsonS=json.dumps(aux)
    return jsonS