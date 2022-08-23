# blueprints/basic_endpoints/__ini__.py
from flask import Blueprint

blueprint = Blueprint('api', __name__, url_prefix='/dbpedia_api')
from flask import request, jsonify
from blueprints.dbpedia_endpoints.key_config import config as kconfig
nlpdb =kconfig.nlpdb
EN = kconfig.MODEL_EMBED

from blueprints.dbpedia_endpoints.extract_key_localdb import  extract_dbpedia


@blueprint.route('/hello_world')
def home():
    return "<h1>API for getting mention terms</h1>"

@blueprint.route('/dbpedia_ranked', methods=['POST'])
def genkeyphrase():

    text = request.data.decode()
    kwdict = extract_dbpedia(text ,nlpdb,EN)
    return jsonify(kwdict)



