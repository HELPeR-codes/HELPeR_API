# blueprints/basic_endpoints/__ini__.py
from flask import Blueprint

blueprint = Blueprint('api', __name__, url_prefix='/gen_api')
from flask import request, jsonify
from blueprints.dbpedia_endpoints.extract_key_localdb import  extract_dbpedia
@blueprint.route('/hello_world')
def home():
    return "<h1>API for getting mention terms</h1>"

@blueprint.route('/genkeyphrase', methods=['POST'])
def genkeyphrase():

    # print("hi")
    text = request.data.decode()
    json_data = None
    topn = 20
    # print(text)
    kwdict = extract_dbpedia(text )
    return jsonify(kwdict)



