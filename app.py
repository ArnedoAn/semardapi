from flask import Flask
from views import data,login,register

app = Flask(__name__)
app.register_blueprint(login)
app.register_blueprint(data)
app.register_blueprint(register)

