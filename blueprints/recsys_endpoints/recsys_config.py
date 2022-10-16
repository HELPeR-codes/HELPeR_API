import pandas as pd
from py2neo import Graph, Relationship
from sentence_transformers import SentenceTransformer
import faiss
from py2neo import NodeMatcher, RelationshipMatcher
import numpy as np
import copy


def getKnowledgeLevel(text):
    if text == "Entry level":
        return 1
    elif text == "Advanced level":
        return 3
    elif text == "Health professional level":
        return 4
    elif text == "Basic":
        return 1
    elif text == "Intermediate":
        return 2
    elif text == "Advanced":
        return 3
    elif text == "Expert":
        return 4
    else:
        return 1

class aconfig:
    connection = None
    __connection = Graph("neo4j://neo4j.ngrok.luozm.me:16002", auth=("neo4j", "helper"))
    local_run = False

    __node_matcher = NodeMatcher(__connection)

    annotation_folder = "/home/luozm/Documents/nursing/online_articles_annotation/"

    SECRET_KEY = "fdsafasd"
    UPLOAD_FOLDER = "image_pool"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # from py2neo.packages.httpstream import SocketError
    # adjust as necessary
    MODEL_EMBED = None
    # initialize sentence transformer model
    MODEL_EMBED = SentenceTransformer('gsarti/biobert-nli')

    # create sentence embeddings
    FAISS_INDEX = None
    # FAISS_INDEX = faiss.read_index("/Users/khushboo/Workspace/helper_web/data/faiss_cpu.index")
    ANY_PHASE = 'Any Phase'

    Rel_TOPIC_NEED = "Has_Topic_level_Need"
    create_user = False
    if create_user:
        __connection.evaluate('''
#         CREATE (n:User {name: 'Mona', 
# 				audienceType: 'patient', 
# 				trajectory:"Previvorship",
# 				pass: '123',
# 				username: 'p2',
# 				uid: '2',
# 				knowledge_level: '1',
# 				age: 'below_50'
# 
# 				})
# 
#         ''')
    #
    #         GRAPHDB.evaluate('''
    #     CREATE (n:User {name: 'Ana',
    # 				audienceType: 'patient',
    # 				trajectory:"Survivorship During Progression/Recurrence",
    # 				pass: '123',
    # 				username: 'p1',
    # 				uid: '1',
    # 				knowledge_level: '1',
    # 				age: 'below_50'
    #
    # 				})
    #
    #         ''')
    #
    #         GRAPHDB.evaluate('''
    # MATCH (t:Topic),(u:User)
    # WHERE u.uid = '1' AND t.text = "management of recurrence"
    # CREATE (u)-[pr:Has_Topic_level_Need]->(t)
    # return u,t
    #
    #         ''')
    #
    #         GRAPHDB.evaluate('''
    # MATCH (t:Topic),(u:User)
    # WHERE u.uid = '1' AND t.text = "symptom treatment related side effect management"
    # CREATE (u)-[pr:Has_Topic_level_Need]->(t)
    # return u,t
    #
    #
    #         ''')

    #         GRAPHDB.evaluate('''
    # MATCH (t:Topic),(u:User)
    # WHERE u.uid = '1' AND t.text = "early menopause"
    # CREATE (u)-[pr:Has_Topic_level_Need]->(t)
    # return u,t
    #
    #
    #         ''')
    #
    #         GRAPHDB.evaluate('''
    #
    # MATCH (t:Topic),(u:User)
    # WHERE u.uid = '1' AND t.text = "targeted therapies"
    # CREATE (u)-[pr:Has_Topic_level_Need]->(t)
    # return u,t
    #         ''')
#     CREATE(n: User
#     {name: 'Angela',
#      audienceType: 'patient',
#      trajectory: "Survivorship (Diagnosis & Treatment)",
#     pass: '123',
#           username: 'Angela',
#     uid: '4',
#     knowledge_level: '1',
#     age: 'above_50',
#     marital_status: 'married',
#     has_caregiver: 'True',
#     cancer_stage: 3,
#     patient_description: 'Angela has recently been diagnosed with stage 3 ovarian cancer. She experienced post menopausal bleeding and was on blood thinner, CT scan with unpromising results. She was worried about the chemotherapy process and the subsequent nausea and mood swings symptoms.'
#
#     })
#
#     ''')
#
#
#
#         GRAPHDB.evaluate('''
#
#
# MATCH(t: Topic), (u:User)
# WHERE
# u.uid = '4'
# AND
# t.text = "nausea"
# CREATE(u) - [pr: Has_Topic_level_Need]->(t)
# return u, t
#
# ''')
#
#
# GRAPHDB.evaluate('''
# MATCH(t: Topic), (u:User)
# WHERE
# u.uid = '4'
# AND
# t.text = "mood swings"
# CREATE(u) - [pr: Has_Topic_level_Need]->(t)
# return u, t
#
# ''')
#
# GRAPHDB.evaluate('''
# MATCH(t: Topic), (u:User)
# WHERE
# u.uid = '4'
# AND
# t.text = "chemotherapy"
# CREATE(u) - [pr: Has_Topic_level_Need]->(t)
# return u, t
#
# ''')
#


    list1 = __connection.evaluate('''
                     MATCH path =(:Topic {text: 'general information'})-[:HasSubTopic*]->(p:Topic)
                    WITH COLLECT(p) AS All
                    MATCH  (m1:Topic)- [:HasSubTopic]->(:Topic)
                    WITH All, COLLECT(m1) AS EXCLUDED
                    RETURN [m1 IN All WHERE NOT m1 IN EXCLUDED] as _results
                ''')

    Topic_ovarian_cancer = [{'name': node['text'], 'id': node['tid']} for node in list1]
    Query_ovarian_cancer = "Ovarian Cancer"
    Topic_append_to_all = []
    for name in ['latest research', 'clinical trials']:
        n = __node_matcher.match("Topic", "v1", "Helper").where(text=name).first()
        Topic_append_to_all.append({'name': n['text'], 'id': n['id']})
    section_df = None
    section_dict = None
    topics_dict = None
    # print(Topic_append_to_all)
    # __document_list = []
    # __document_dict = {}
    # nodes = __node_matcher.match("Document", "v1", "Helper")
    # print(len(nodes))
    # for nodedoc in nodes:
    #     __document_dict[nodedoc['did']] = {
    #         'did': nodedoc['did'],
    #         'trajectory': nodedoc['trajectory'],
    #         'doc_title': nodedoc['title'],
    #         'url': nodedoc['url'],
    #         'audienceType': nodedoc['audienceType'],
    #         'knowledgeLevel': getKnowledgeLevel(nodedoc['knowledgeLevel']),
    #     }
    #
    #     __document_list.append(
    #         {
    #             'did': nodedoc['did'],
    #             'trajectory': nodedoc['trajectory'],
    #             'doc_title': nodedoc['title'],
    #             'url': nodedoc['url'],
    #             'audienceType': nodedoc['audienceType'],
    #             'knowledgeLevel': getKnowledgeLevel(nodedoc['knowledgeLevel']),
    #         }
    #     )
    #
    # __document_df = pd.DataFrame(__document_list)
    # section_dict = {}
    # __section_list = []
    # nodes = __node_matcher.match("Section")
    # # print(len(nodes))
    # for node in nodes:
    #     nodedoc = __connection.evaluate('''
    #      Match (n:Document) - [r] - (s:Section) where s.sid = '{&sid}' return n limit 1
    #     '''.replace("{&sid}", node['sid']))
    #     if type(nodedoc) is list:
    #         nodedoc = nodedoc[0]
    #     # print(nodedoc)
    #
    #     nodetopic = __connection.evaluate('''
    #              Match (n:Topic) - [r] - (s:Section) where s.sid = '{&sid}'  return n limit 1
    #             '''.replace("{&sid}", node['sid']))
    #     if nodetopic is None:
    #         print(" very important - section with id " + node['sid'] + " has no topic")
    #         continue
    #
    #     section_details = {
    #
    #         'sid': node['sid'],
    #         'text': ' '.join(node['text'].split(" ")[0:200]),
    #         'text2send': ' '.join(node['text'].split(" ")[0:100]),
    #         'topic': nodetopic['text'],
    #         'tid': nodetopic['id']
    #     }
    #     if 'embed' in node:
    #         section_details['embed'] = np.array([(s) for s in node['embed'][1:-1].split()]).astype(np.float32)
    #
    #     for key in __document_dict[nodedoc['did']]:
    #         section_details[key] = __document_dict[nodedoc['did']][key]
    #
    #     if 'embed' not in section_details :
    #         search_text = section_details['topic'] + " [SEP] " + section_details['doc_title'] + " [SEP] " + \
    #                       section_details['text']
    #         sentence_embeddings = MODEL_EMBED.encode(search_text)
    #
    #         tw_dict = {'embed': np.array_str(sentence_embeddings)}
    #         existingsection = __node_matcher.match('Section', sid=section_details['sid']).first()
    #         section_details['embed'] = sentence_embeddings
    #
    #         if existingsection:
    #             existingsection.update(**tw_dict)
    #             __connection.push(existingsection)
    #
    #     __section_list.append(copy.copy(section_details))
    #     section_dict[node['sid']] = section_details
    # section_df = pd.DataFrame(__section_list)
    #
    # # Topic List
    # topics = __node_matcher.match('Topic', 'v1')
    # topics_dict = {}
    # for topic in topics:
    #     tid = topic['id']
    #     topics_dict[tid] = {}
    #     subtopics = __connection.evaluate('''
    #     MATCH (p:Topic{id:"{&id}"})-[:HasSubTopic*0..2]->(c)
    #     RETURN {parent : p.id, child : {id :collect( c.id)}}
    #     '''.replace("{&id}", str(tid)))
    #     if subtopics is not None:
    #         topics_dict[tid] = [child for child in subtopics['child']['id']]

    columns_to_return = ['did','sid','tid','topic','text2send','score','doc_title','url','audienceType','knowledgeLevel','trajectory']