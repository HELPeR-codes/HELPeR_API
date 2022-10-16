# blueprints/basic_endpoints/__ini__.py
from flask import Blueprint
from flask import request, jsonify
blueprint = Blueprint('api', __name__, url_prefix='/basic_api')
from blueprints.basic_endpoints.role_config import  rconfig
nlp_role =rconfig.NLP_role
rtokenizer = rconfig.tokenizer
role_models = rconfig.role_models
from blueprints.basic_endpoints.extract_role import extract_roles

@blueprint.route('/hello_world')
def home():
    return "<h1>API for getting mention terms</h1>"

@blueprint.route('/role', methods=['POST'])
def role():

    # print("hi")
    text = request.data.decode()
    json_data = None
    topn = 20
    print(text)
    output = extract_roles(text=text,nlp_role=nlp_role,role_models=role_models,rtokenizer=rtokenizer)

    return jsonify(str(output))

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



