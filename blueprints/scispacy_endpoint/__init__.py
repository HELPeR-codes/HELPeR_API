# blueprints/basic_endpoints/__ini__.py
from flask import Blueprint
blueprint = Blueprint('med_api', __name__, url_prefix='/med_api')
from flask import request, jsonify
import logging
from blueprints.scispacy_endpoint.keyphrase import  extract_med_key
from blueprints.scispacy_endpoint.med_config import aconfig as kconfig


@blueprint.route('/top_n_entities', methods=['POST','GET'])
def get_keyphrases():

    text = request.data.decode()
    logging.warning(" data input : "+text)

    kwdict = extract_med_key(10,text )
    return jsonify(kwdict)

    kw_json = recommend(dict_input)
    return kw_json


