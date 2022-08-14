# blueprints/basic_endpoints/__ini__.py
from flask import Blueprint

blueprint = Blueprint('recsys_api', __name__, url_prefix='recsys_api')
from flask import request, jsonify

from blueprints.recsys_endpoints.recsys import search, recommend
@blueprint.route('/hello_world')
def home():
    return "<h1>API for getting mention terms</h1>"

@blueprint.route('/search', methods=['POST'])
def get_search():

    text = request.data.decode()
    kw_json = search(text)
    return kw_json

@blueprint.route('/rec', methods=['POST'])
def get_rec():

    text = request.data.decode()
    kw_json = recommend(text)
    return kw_json

