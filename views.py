from flask import Blueprint, jsonify, request, send_file
import Util
from flask_cors import cross_origin


main = Blueprint('main', __name__)

@main.route('/')
@cross_origin()
def get_vehicles():
    return Util.getVehicles()