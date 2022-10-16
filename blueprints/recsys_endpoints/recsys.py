import blueprints

from blueprints.recsys_endpoints.recsys_config import aconfig as config
from blueprints.recsys_endpoints.recsys_config import getKnowledgeLevel
import json
from sentence_transformers import util
annotation_folder = config.annotation_folder
import copy
from flask import json
from blueprints.recsys_endpoints.recsys_utilities import  get_neo4jNodeMatcher, get_neo4jRelationshipMatcher, get_neo4jConnection as graph
import pandas as pd
model = config.MODEL_EMBED
findex = config.FAISS_INDEX
import logging

import numpy as np

def get_user_topic_interest(usernode):
    rel_matcher = get_neo4jRelationshipMatcher()
    topic_score={}
    for rel in rel_matcher.match((usernode,None), config.Rel_TOPIC_NEED):
        score = 0
        if rel['int_score']  :
            score = float(rel['int_score'])
        topic_score[rel.end_node['id']] = score

    return topic_score

def get_user_detail(userid):
    node_matcher = get_neo4jNodeMatcher()
    usernode = node_matcher.match("User").where(uid=userid).first()

    if usernode is None:
        return {}
    trajectory = 'Survivorship'
    logging.warning("Getting details for " +usernode['name'])
    if 'trajectory' in usernode.keys():
        trajectory = usernode['trajectory']

    need=list({'name':r.end_node["text"],'id':r.end_node['id']} for r in graph().match(nodes=(usernode,),r_type=config.Rel_TOPIC_NEED))
    if need == None or len(need) == 0:
        need = config.Topic_ovarian_cancer
    logging.warning( str(need))
    for topic in config.Topic_append_to_all:
        if topic not in need:
            need.append(topic)

    return {'name':usernode['name'], 'trajectory':trajectory,'topics': need,'audienceType':usernode['audienceType'],'knowledgeLevel':usernode['knowledge_level'],
            'age':usernode['age'],
            'topic_score':get_user_topic_interest(usernode)}


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
    if len(user_details) == 0:
        return {'error': 'user not found in the system'}
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
        topic_data = topic_data[config.columns_to_return].sort_values(by=['score','knowledgeLevel'],ascending=[False,True]).head(30).reset_index()
        if len(topic_data) ==
        topic_data = topic_data.groupby('did',as_index=False).agg('first')
        topic_data = topic_data.set_index("item_"+topic_data.index.astype(str))
        jsontemp = copy.copy(topic_data.to_dict('index'))

        result_return[topic['name']]={}
        result_return[topic['name']]['results'] = jsontemp

        tid_pre_score = 0
        score_now = topic_data['score'].head(3).mean()

        if topic['id'] in user_details['topic_score']:
            tid_pre_score = user_details['topic_score'][topic['id']]


        result_return[topic['name']]['mean_3'] =  0 if np.isnan(score_now) else score_now
        result_return[topic['name']]['score'] = score_now if tid_pre_score is None or np.isnan(tid_pre_score) else tid_pre_score
        result_return[topic['name']]['size'] = len(topic_data['score'])

    return result_return

def get_user_search(userid, data,query):
    print(len(data))
    user_details = get_user_detail(userid)
    if len(user_details) == 0:
        return {'error': 'user not found in the system'}

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
    topics = list(data.groupby(['topic']).count().sort_values(['score'], ascending=False).head(4).index)

    for topic in topics:
        topic_data = data[data['topic'] == topic]

        topic_data = topic_data[config.columns_to_return].sort_values(by=['score','knowledgeLevel'],ascending=[False,True]).head(20).reset_index()
        topic_data = topic_data.set_index("item_"+topic_data.index.astype(str) )
        jsontemp = copy.copy(topic_data.to_dict('index'))
        result_return[topic]={}
        result_return[topic]['results'] = jsontemp

        tid_pre_score = 0
        score_now = topic_data['score'].head(3).mean()

        if topic['id'] in user_details['topic_score']:
            tid_pre_score = user_details['topic_score']


        result_return[topic['name']]['mean_3'] =  0 if np.isnan(score_now) else score_now

        result_return[topic['name']]['score'] = score_now if np.isnan(tid_pre_score) else tid_pre_score
        result_return[topic]['size'] = len(topic_data['score'])

    return result_return

def get_topic_list(topic):

    data=config.section_df
    result_return={}
    # topic_data= data
    data = copy.copy(data[data['tid'].isin(config.topics_dict[topic['id']])])

    #print("topic",topic['name'],len(topic_data))

    topic_query = topic['text']
    topic_embed = config.MODEL_EMBED.encode(topic_query)

    scores = similarity_search(topic_embed,data['embed'])
    data['score'] = scores
    data = data[config.columns_to_return].sort_values(by=['score'],ascending=[False]).head(40).reset_index()

    topic_data = data.set_index("item_"+data.index.astype(str) )
    jsontemp = copy.copy(topic_data.to_dict('index'))
    result_return[topic['name']]={}
    result_return[topic['name']]['results'] = jsontemp

    score_now = topic_data['score'].head(10).mean()

    result_return[topic['name']]['score'] = score_now
    result_return[topic]['size'] = len(topic_data['score'])

    return result_return

def get_topic_search(data,query):

    print(len(data))

    result_return={}
    # topic_data= data
    #topic_data = copy.copy(data[data['tid'].isin(config.topics_dict[topic['id']])])
    #print("topic",topic['name'],len(topic_data))
    topic_query = query +" [SEP] Ovarian Cancer"
    topic_embed = config.MODEL_EMBED.encode(topic_query)

    scores = similarity_search(topic_embed,data['embed'])
    data['score'] = scores
    data = data[config.columns_to_return].sort_values(by=['score'],ascending=[False]).head(100).reset_index()
    topics = list(data.groupby(['topic']).count().sort_values([['score']], ascending=False).head(1).index)

    for topic in topics:
        topic_data = data[data['topic'] == topic]

        topic_data = topic_data[config.columns_to_return].sort_values(by=['score'],ascending=[False]).head(10).reset_index()
        topic_data = topic_data.set_index("item_"+topic_data.index.astype(str) )
        jsontemp = copy.copy(topic_data.to_dict('index'))
        result_return[topic]={}
        result_return[topic]['results'] = jsontemp

        tid_pre_score = 0
        score_now = topic_data['score'].head(10).mean()

        result_return[topic['name']]['score'] = tid_pre_score
        result_return[topic]['size'] = len(topic_data['score'])

    return result_return

def recommend(input):

    kw = None
    utype = None
    filtersections = config.section_df
    if filtersections is None or len(filtersections) == 0:
        print("No documents in the collection - reloading new")
        reload()

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

def recommend_topic(input):

    kw = None
    utype = None
    filtersections = config.section_df

    query = None
    topic = None
    if 'topic' in input:
        topic = input['topic']

    else:
        return "Topic not mentioned - so default topic is"

    if not topic in config.topics_dict:
            return "Topic not mentioned - so default topic is"
    topic_obj = config.topics_dict[topic]
    results = get_topic_list(topic=topic_obj, data=filtersections,query=query)

    return json.dumps(results)

def reload():
    message="None"

    try:
        node_matcher =get_neo4jNodeMatcher()
        list1 = graph().evaluate('''
                             MATCH path =(:Topic {text: 'general information'})-[:HasSubTopic*]->(p:Topic)
                            WITH COLLECT(p) AS All
                            MATCH  (m1:Topic)- [:HasSubTopic]->(:Topic)
                            WITH All, COLLECT(m1) AS EXCLUDED
                            RETURN [m1 IN All WHERE NOT m1 IN EXCLUDED] as _results
                        ''')

        config.Topic_ovarian_cancer = [{'name': node['text'], 'id': node['tid']} for node in list1]
        config.Topic_append_to_all = []
        for name in ['latest research', 'clinical trials']:

            n = node_matcher.match("Topic", "v1", "Helper").where(text=name).first()
            config.Topic_append_to_all.append({'name': n['text'], 'id': n['id']})


        document_list = []
        document_dict = {}
        nodes = node_matcher.match("Document", "v1", "Helper", type="annotated")
        print(len(nodes))
        for nodedoc in nodes:
            document_dict[nodedoc['did']] = {
                'did': nodedoc['did'],
                'trajectory': nodedoc['trajectory'],
                'doc_title': nodedoc['title'],
                'url': nodedoc['url'],
                'audienceType': nodedoc['audienceType'],
                'knowledgeLevel': getKnowledgeLevel(nodedoc['knowledgeLevel']),
            }

            document_list.append(
                {
                    'did': nodedoc['did'],
                    'trajectory': nodedoc['trajectory'],
                    'doc_title': nodedoc['title'],
                    'url': nodedoc['url'],
                    'audienceType': nodedoc['audienceType'],
                    'knowledgeLevel': getKnowledgeLevel(nodedoc['knowledgeLevel']),
                }
            )

        document_df = pd.DataFrame(document_list)
        section_dict = {}
        section_list = []

        if config.local_run == True:
            nodes = node_matcher.match("Section").limit(100)
        else:
            nodes = node_matcher.match("Section")
        # print(len(nodes))
        for node in nodes:
            nodedoc = graph().evaluate('''
             Match (n:Document) - [r] - (s:Section) where s.sid = '{&sid}' return n limit 1
            '''.replace("{&sid}", node['sid']))
            if nodedoc is None:
                print("no node doc")
                print("skip this section ")
                continue

            if type(nodedoc) is list:
                nodedoc = nodedoc[0]

            # print(nodedoc)

            nodetopic = graph().evaluate('''
                     Match (n:Topic) - [r] - (s:Section) where s.sid = '{&sid}'  return n limit 1
                    '''.replace("{&sid}", node['sid']))

            if nodetopic is None:
                print(" very important - section with id " + node['sid'] + " has no topic")
                continue

            # print(nodetopic)
            section_details = {

                'sid': node['sid'],
                'text': ' '.join(node['text'].split(" ")[0:200]),
                'text2send': ' '.join(node['text'].split(" ")[0:200]),
                'topic': nodetopic['text'],
                'tid': nodetopic['id']
            }
            # print(section_details)
            if 'embed' in node:
                section_details['embed'] = np.array([(s) for s in node['embed'][1:-1].split()]).astype(np.float32)

            for key in document_dict[nodedoc['did']]:
                section_details[key] = document_dict[nodedoc['did']][key]

            if 'embed' not in section_details:
                search_text = section_details['topic'] + " [SEP] " + section_details['doc_title'] + " [SEP] " + \
                              section_details['text']
                sentence_embeddings = config.MODEL_EMBED.encode(search_text)

                tw_dict = {'embed': np.array_str(sentence_embeddings)}
                existingsection = node_matcher.match('Section', sid=section_details['sid']).first()
                section_details['embed'] = sentence_embeddings

                if existingsection:
                    existingsection.update(**tw_dict)
                    graph().push(existingsection)

            section_list.append(copy.copy(section_details))
            section_dict[node['sid']] = copy.copy(section_details)
        section_df = pd.DataFrame(section_list)

        # Topic List
        topics = node_matcher.match('Topic', 'v1')
        topics_dict = {}
        for topic in topics:
            tid = topic['id']
            topics_dict[tid] = {}
            subtopics = graph().evaluate('''
            MATCH (p:Topic{id:"{&id}"})-[:HasSubTopic*0..2]->(c) 
            RETURN {parent : p.id, child : {id :collect( c.id)}}
            '''.replace("{&id}", str(tid)))
            if subtopics is not None:
                topics_dict[tid] = [child for child in subtopics['child']['id']]

        config.section_df = copy.copy(section_df)
        config.section_dict = copy.copy(section_dict)
        config.topics_dict = copy.copy(topics_dict)

        usernodes = node_matcher.match("User", "v1", "Helper")
        for node in usernodes:
            update_user_topic_score(node['uid'])


        message="Reload looks successful"




    except:
        message = "Error while reloading = Please check"
        print(message)


    return message

def update_user_topic_score(user_id):
    message="None"
    node_matcher = get_neo4jNodeMatcher()
    rel_matcher = get_neo4jRelationshipMatcher()
    usernode = node_matcher.match("User").where(uid=user_id).first()

    try:
        results = get_user_recommendation(userid=user_id,data=config.section_df)
        new_score = 0
        for rel in rel_matcher.match((usernode, None), config.Rel_TOPIC_NEED):
            topic = rel.end_node['text']
            if topic in results:
                new_score = results[topic]['mean_3']
            old_score = 0
            if rel['int_score'] :
                old_score = float(rel['int_score'])

            if new_score != old_score:
                rel['int_score'] = str(new_score)
                graph().push(rel)

        message="updated user details"
    except:
        message = "Error while updating scores = Please check"
        print(message)


    return message

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

    # update_user_topic_score('2')
    # update_user_topic_score('1')
    # update_user_topic_score('3')
    # a = recommend({'userid':'1'})
    # print(a)

    # a = recommend_topic({'topic':"chemotherapy"})
    # print(a)

    # print(a)
    # print(len(a))
    # config.connection = None
    # a = recommend({'userid':'1'})
    # print(len(a))
    # message = reload()
    a = recommend_topic({'topic':'surgery'})

    print(len(a))
