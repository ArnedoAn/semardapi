from flask import Blueprint
from database.dbController import *
from controllers.jwtController import token_required

dataEndP = Blueprint('dataEndP', __name__, template_folder='templates')

@dataEndP.route('/setdata', methods=['POST'])
@token_required
def set():
    return setData()

@dataEndP.route('/alldata')
@token_required
def allData():
    return getLastOne()

@dataEndP.route('/lastone')
def lastOne():
    return getLastOne()
