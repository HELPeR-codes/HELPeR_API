# blueprints/basic_endpoints/__ini__.py
from flask import Blueprint

blueprint = Blueprint('api', __name__, url_prefix='/basic_api')
from flask import request, jsonify
from blueprints.basic_endpoints.role_config import  rconfig
nlp_role =rconfig.NLP_role
rtokenizer = rconfig.tokenizer
role_models = rconfig.role_models
from blueprints.basic_endpoints.extract_role import extract_roles

@blueprint.route('/hello_world')
def home():
    return "<h1>API for getting mention terms</h1>"

# @app.route('/genkeyphrase', methods=['POST'])
# def genkeyphrase():
#
#     # print("hi")
#     text = request.data.decode()
#     json_data = None
#     topn = 20
#     # print(text)
#     kwdict = extract_dbpedia(text ,nlpdb,EN)
#     return jsonify(kwdict)

@blueprint.route('/role', methods=['POST'])
def extract_post_roles():

    text = request.data.decode()
    kwdict = extract_roles(text,nlp_role,role_models,rtokenizer )
    kwdict = {str(key): str(value) for key, value in kwdict.items()}
    print(kwdict)
    return jsonify(kwdict)


