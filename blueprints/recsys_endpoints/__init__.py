# blueprints/basic_endpoints/__ini__.py
from flask import Blueprint
import json
blueprint = Blueprint('recsys_api', __name__, url_prefix='/recsys_api')
from flask import request, jsonify
import logging
from blueprints.recsys_endpoints.recsys import  recommend, reload, recommend_topic
from blueprints.recsys_endpoints.recsys_config import aconfig as config
# @blueprint.route('/hello_world')
# def home():
#     return "<h1>API for getting mention terms</h1>"
from apscheduler.schedulers.background import BackgroundScheduler

reload()

@blueprint.route('/rec', methods=['POST','GET'])
def get_rec():
    dict_input = {}
    print(request.method)
    if request.method == "POST":
        if request.json:
            dict_input=json.loads(request.json)
    else:
            print("In get")
            print(request.data)
            print("hi")
            if request.args.get('userid'):
                dict_input['userid'] = request.args.get('userid')
            if request.args.get('kw'):
                dict_input['kw'] = str(request.args.get('kw').split(","))
            if request.args.get('utype'):
                dict_input['utype'] = str(request.args.get('utype').split(","))
            if request.args.get('query'):
                dict_input['query'] = request.args.get('query')

    logging.warning(" data input : "+str(dict_input))

    kw_json = recommend(dict_input)
    return kw_json

@blueprint.route('/list_topic_docs', methods=['POST','GET'])
def get_rec():
    dict_input = {}
    print(request.method)
    if request.method == "POST":
        if request.json:
            dict_input=json.loads(request.json)
            if 'topic' in dict_input:
                dict_input['query'] = dict_input['topic']
            else:
                dict_input['query'] = config.Query_ovarian_cancer
    else:
            print("In get")
            print(request.data)
            print("hi")
            if request.args.get('topic'):
                dict_input['topic'] = request.args.get('topic')

    logging.warning(" data input : "+str(dict_input))

    kw_json = recommend_topic(dict_input)
    return kw_json


@blueprint.route('/reload', methods=['POST','GET'])
def get_reload():
    message = reload()
    print("reloaded")
    print(message)
    return {"done":message}

scheduler = BackgroundScheduler()
job = scheduler.add_job(get_reload, 'interval', hours = 24)
scheduler.start()