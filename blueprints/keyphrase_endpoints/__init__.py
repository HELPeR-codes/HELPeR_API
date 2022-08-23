# blueprints/basic_endpoints/__ini__.py
from flask import Blueprint

blueprint = Blueprint('api', __name__, url_prefix='/key_api')
from flask import request, jsonify
from blueprints.keyphrase_endpoints.key_config import config as kconfig
nlpdb =kconfig.nlpdb
EN = kconfig.MODEL_EMBED



from blueprints.basic_endpoints.extract_role import extract_roles

@blueprint.route('/hello_world')
def home():
    return "<h1>API for getting mention terms</h1>"

@blueprint.route('/genkeyphrase', methods=['POST'])
def genkeyphrase():

    text = request.data.decode()
    json_data = None
    topn = 20
    kwdict = extract_dbpedia(text ,nlpdb,EN)
    return jsonify(kwdict)



