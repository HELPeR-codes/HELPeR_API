# blueprints/basic_endpoints/__ini__.py
from flask import Blueprint
import json
blueprint = Blueprint('recsys_api', __name__, url_prefix='/recsys_api')
from flask import request, jsonify
import logging
from blueprints.recsys_endpoints.recsys import  recommend

# @blueprint.route('/hello_world')
# def home():
#     return "<h1>API for getting mention terms</h1>"


@blueprint.route('/rec', methods=['POST','GET'])
def get_rec():
    dict_input={}
    for arg in request.args.keys():
        logging.warning( "input: " + arg +" : " + request.args.get(arg))
        dict_input[arg] = request.args.get(arg)

    logging.warning(" data input : ")
    kw_json = recommend(dict_input)
    return kw_json

