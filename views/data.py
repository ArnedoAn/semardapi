from flask import Blueprint, request, jsonify, render_template
from database import *
from controllers import token_required

data = Blueprint('data', __name__, template_folder='templates')

@data.route('/setdata', methods=['POST'])
@token_required
def set():
    setData()

@data.route('/alldata')
@token_required
def allData():
    getLastOne()

@data.route('/lastone')
def lastOne():
    getLastOne()
