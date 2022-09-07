from flask import Flask
from views.data import *
from views.login import *
from views.register import *
from views.home import *
from database.dbController import helloW

app = Flask(__name__)

app.register_blueprint(loginEndP)
app.register_blueprint(dataEndP)
app.register_blueprint(registerEndP)
app.register_blueprint(homeEndP)

