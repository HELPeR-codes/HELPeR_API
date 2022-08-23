from blueprints.recsys_endpoints.recsys_config import aconfig as config
import json
from sentence_transformers import util
annotation_folder = config.annotation_folder
import copy
from flask import json

model = config.MODEL_EMBED
findex = config.FAISS_INDEX
graph = config.GRAPHDB
import logging
node_matcher = config.node_matcher

def get_user_detail(userid):
    usernode = node_matcher.match("User").where(uid=userid).first()

    trajectory = 'Survivorship'
    logging.warning("Getting details for " +usernode['name'])
    if 'trajectory' in usernode.keys():
        trajectory = usernode['trajectory']

    need=list({'name':r.end_node["text"],'id':r.end_node['id']} for r in graph.match(nodes=(usernode,),r_type=config.Rel_TOPIC_NEED))
    if need == None or len(need) == 0:
        need = config.Topic_ovarian_cancer
    logging.warning( str(need))
    for topic in config.Topic_append_to_all:
        if topic not in need:
            need.append(topic)

    return {'name':usernode['name'], 'trajectory':trajectory,'topics': need,'audienceType':usernode['audienceType'],'knowledgeLevel':usernode['knowledge_level'],'age':usernode['age']}


def search(query):
    xq = model.encode([query])
    D, I = findex.search(xq, k=5)  # search
    print(D)
    return [key for key in I[0]]

def similarity_search(query_embed,docs_embed):
    sectionwise_score=[]
    for doc in docs_embed:
        sectionwise_score.append(round(util.pytorch_cos_sim(query_embed, doc).item(),2))

    return sectionwise_score


def get_sections_detail(sections):
    section_dict = config.section_dict
    print(sections)
    for section in sections:
        section_details = section_dict[section['sid']]
        for key,value in section_details.items():
            section[key] = value


    return sections


def get_user_recommendation(userid, data):
    print(len(data))
    user_details = get_user_detail(userid)
    needs_topic = user_details['topics']
    trajectory = user_details['trajectory']
    data = data[data['trajectory'].isin([trajectory,config.ANY_PHASE])]
    print(len(data))
    result_return={}
    for topic in needs_topic:
        topic_data = copy.copy(data[data['tid'].isin(config.topics_dict[topic['id']])])
        print("topic",topic['name'],len(topic_data))
        user_topic_query = topic['name'] +" [SEP] Ovarian Cancer"
        user_embed = config.MODEL_EMBED.encode(user_topic_query)
        scores = similarity_search(user_embed,topic_data['embed'])
        topic_data['score'] = scores
        topic_data = topic_data[config.columns_to_return].sort_values(by=['score','knowledgeLevel'],ascending=[False,True]).head(10).reset_index()
        topic_data = topic_data.set_index("item_"+topic_data.index.astype(str) )
        jsontemp = copy.copy(topic_data.to_dict('index'))

        result_return[topic['name']]={}
        result_return[topic['name']]['results'] = jsontemp
        result_return[topic['name']]['score'] = topic_data['score'].head(3).mean()
        result_return[topic['name']]['size'] = len(topic_data['score'])

    return result_return

def get_user_search(userid, data,query):
    print(len(data))
    user_details = get_user_detail(userid)

    trajectory = user_details['trajectory']
    data = data[data['trajectory'].isin([trajectory,config.ANY_PHASE])]
    print(len(data))
    result_return={}

    # topic_data= data
    #topic_data = copy.copy(data[data['tid'].isin(config.topics_dict[topic['id']])])
    #print("topic",topic['name'],len(topic_data))
    user_topic_query = query +" [SEP] Ovarian Cancer"
    user_embed = config.MODEL_EMBED.encode(user_topic_query)
    scores = similarity_search(user_embed,data['embed'])
    data['score'] = scores
    data = data[config.columns_to_return].sort_values(by=['score'],ascending=[False]).head(40).reset_index()
    topics = list(data.groupby(['topic']).count().sort_values(['did'], ascending=False).head(4).index)
    #print(topics)
    for topic in topics:
        topic_data = data[data['topic'] == topic]
        topic_data = topic_data[config.columns_to_return].sort_values(by=['score','knowledgeLevel'],ascending=[False,True]).head(10).reset_index()
        topic_data = topic_data.set_index("item_"+topic_data.index.astype(str) )
        jsontemp = copy.copy(topic_data.to_dict('index'))
        result_return[topic]={}
        result_return[topic]['results'] = jsontemp
        result_return[topic]['score'] = topic_data['score'].head(3).mean()
        result_return[topic]['size'] = len(topic_data['score'])

    return result_return


def recommend(input):
    kw = None
    utype = None
    filtersections = config.section_df
    if 'kw' in input:
        kw = eval(input['kw'])
        filtersections = filtersections[ filtersections['knowledgeLevel'].isin(kw)]

    if 'utype' in input:
        utype = eval(input['utype'])
        filtersections = filtersections[filtersections['audienceType'].isin(utype)]

    if 'userid' not in input:
        print("No user sent")
        return {"error":"No userid sent"}

    query = None
    if 'query' in input:
        query = input['query']
    if query == None or query == '':
        results = get_user_recommendation(userid=input['userid'],data=filtersections)

    else:
        results = get_user_search(userid=input['userid'], data=filtersections,query=query)

    return json.dumps(results)


if __name__ == '__main__':
    # a=get_user_detail('1')
    # print(a)
    # print(len(a['topics']))
    # a = get_user_detail('2')
    # print(a)
    # print(len(a['topics']))
    # ranklist = [{'sid':'5ac97e6d108a8e2887c00083877df5ab82decd4c','rank':1},{'sid':'4526d62236cee7be109803d49b6cd2aeadeab6d2','rank':2}]
    # sections = get_sections_detail(ranklist)
    # print(sections)
    a = recommend({'userid':'1','kw':'[1,2,3]','utype':'["patient","caregiver","patient and caregiver","Health professional"]','query':"hair loss and pain during chemotherapy"})
    print(a)

