import pandas as pd
import datetime as dt2
from datetime import datetime
from blueprints.recsys_endpoints.recsys_config import aconfig
import json
import pathlib
import copy

annotation_folder = aconfig.annotation_folder

from flask import json
import numpy as np
import pandas as pd
from py2neo import Node,Relationship,Graph,Path,Subgraph
from py2neo import NodeMatcher,RelationshipMatcher

def get_user_detail(name):

    node_matcher = NodeMatcher(graph)
    node = node_matcher.match("User").where(name=name).first()
    trajectory='Any Phase'
    need = [ 'Ovarian Cancer' ]
    print(node['name'])
    if 'trajectory' in node.keys():
        trajectory=node['trajectory']

    if 'need' in node.keys():
        need = [x.strip() for x in node['need'].split(",")]

    return [name,trajectory,need]

from config import MODEL_EMBED as model
from config import FAISS_INDEX as findex
def get_embedding(search_text):
    sentence_embeddings = model.encode(search_text.to_list())
    return sentence_embeddings

def search(query):
    xq=model.encode([query])
    D, I = findex.search(xq,k=5)  # search
    print(D)
    return [  key  for key in I[0]]

def get_sections_detail(sections):
    node_matcher = NodeMatcher(graph)
    result=[]
    did = []
    for key in sections:
        node = node_matcher.match("Section").where(unique_id=int(key)).first()
        if node['did'] not in did:
            did.append(node['did'])
            result.append([node['did'],node['trajectory'],node['title'],node['url'],node['search_topic'],node['name']])

    return result


def get_user_recommendation(trajectory,need):
    query = trajectory + " [SEP] " + need + ' [SEP] '
    a = search(query)
    print(a)
    if trajectory != 'Any Phase':
        print("resort")
    return get_sections_detail(a)


def updates(from_date):
    dt=None
    try:
        dt = datetime.strptime(from_date,"%m-%d-%Y")
    except Exception:
        print("cannot parse date ")
        return json.dumps({"error":"not able to parse date"})

    # print(dt,datetime.now())

    if dt > datetime.now():
        return json.dumps({"error":"future date"})

    if dt is None:
        return json.dumps({"error":"none date"})
    df_latest=None
    df = None
    startdate=dt
    enddate = datetime.now()
    while startdate < enddate:
        for file in list(pathlib.Path(annotation_folder).glob('*_daily_'+datetime.strftime(startdate,"%y_%-m_%-d")+'*')):
            dftemp = pd.read_json(file)
            dftemp['date']=startdate
            if df is None:
                df=copy.copy(dftemp)
            else:
                df = pd.concat([df,copy.copy(dftemp)])
        startdate = startdate + dt2.timedelta(days=1)
    if df is not None:
        df_latest = df.sort_values('date').drop_duplicates('id', keep='last')
        print("No of json objects sent", len(df_latest))
        return df_latest.to_json(orient="records")
    return {}


if __name__ == '__main__':
    # a = updates(from_date="04-18-2022")
    # print(a)

    a= updates(from_date="01-01-2020")
    print(a)





