# blueprints/basic_endpoints/__ini__.py
from flask import Blueprint

blueprint = Blueprint('annotation_api', __name__, url_prefix='/annotation_api')
from flask import request, jsonify

from blueprints.annotation_endpoints.get_annotations import updates
@blueprint.route('/hello_world')
def home():
    return "<h1>API for getting mention terms</h1>"

@blueprint.route('/updates', methods=['POST'])
def extract_post_roles():

    text = request.data.decode()
    kw_json = updates(text)
    return kw_json


