import pandas as pd

print("load model")
import requests
# initialize language model
from blueprints.dbpedia_endpoints.key_config import config
import operator
from blueprints.dbpedia_endpoints.db_util import  preprocessText, get_abstract, get_type, scoring, remove_html,write_notused,get_wikipage
import json
import os
import numpy as np


import time
def extract_dbpedia(text, nlpdb, EN):
    # print(text)
    text = preprocessText(text,lower=False,stemming=False)
    doc = nlpdb(text)
    cols=['concept','tf','dbpedia_url','desc','sim_score','db_link_score','wikipage',
          'duplicates','types','is_filtered',
          'reason_score','reason_type','reason_link','overall_score','reason_wikipage']
    db_entities = pd.DataFrame({},columns=cols)
    uentities = {}
    # minsc = +1
    # maxsc = -1
    # dbpedia_page = []
    # dbpedia_page_not_selected=[]
    entity_concept={}
    entities_list=[]

    for ent in doc.ents:
        print(ent.text)

    for ent in doc.ents:
        # dup = 0
        alltypes = []
        wikipage = None


        ent_text = ent.text.lower()
        if ent_text not in entities_list:
            entities_list.append(ent_text)

            if ent.kb_id_ in list(db_entities['dbpedia_url'].unique()):
                temp_entity = db_entities[db_entities['dbpedia_url'] == ent.kb_id_].iloc[0]
                uentities[temp_entity['concept']]['duplicates'].append(ent_text)
                db_entities = pd.DataFrame.from_dict(uentities, orient='index')
                entity_concept[ent_text]=temp_entity['concept']
                continue

            #removed abstract extraction -taking too much time
            scor = scoring([ent.text, text], EN)

            linkscore = 1
            if ent and ent._.dbpedia_raw_result and ent._.dbpedia_raw_result['@similarityScore']:
                linkscore = float(ent._.dbpedia_raw_result['@similarityScore'])


            if ent and ent._.dbpedia_raw_result and ent._.dbpedia_raw_result['@types']:
                abc = ent._.dbpedia_raw_result['@types'].split(",")
                for x in abc:
                    if "DBpedia:" in x:
                        alltypes.append(x.split("DBpedia:")[1])

            # a = get_type(ent.kb_id_)
            # if a is not None:
            #     for obj in a['results']['bindings']:
            #         alltypes.append(obj['obj']['value'].split("/")[-1])

            # if len(set(alltypes).intersection(config.types_not_allowed)) > 0:
            #     continue

            # if ent.kb_id_ is not None and "dbpedia" in ent.kb_id_:
            #     data = requests.get(ent.kb_id_.replace("/resource/", "/data/") + ".json").json()
            #     dbpedia_json = data[ent.kb_id_]
            #     if 'http://xmlns.com/foaf/0.1/isPrimaryTopicOf' in dbpedia_json:
            #         wikipage = dbpedia_json['http://xmlns.com/foaf/0.1/isPrimaryTopicOf'][0]['value']
                    # print(wikipage)


            uentities[ent_text] = {'concept': ent_text,
                                   'tf': 1,
                                   'duplicates':[],
                                   'sim_score':scor,
                                   'db_link_score':linkscore,
                                   'wikipage': wikipage,
                                   'types': list(set(alltypes)),
                                   'overall_score':round(np.mean([scor,linkscore]),5),
                                   'dbpedia_url':ent.kb_id_,
                                   'is_filtered':0
                                   }


            if scor < config.sim_score:
                # print(ent_text,scor,ent.kb_id_,"removed because of low score")
                uentities[ent_text]['is_filtered'] = 1
                uentities[ent_text]['reason_score'] = "low sim score"

            if linkscore < config.link_score:
                # print(ent_text, linkscore, ent.kb_id_,"removed because of low links score")
                uentities[ent_text]['is_filtered'] = 1
                uentities[ent_text]['reason_link'] = "low link score"

            if len(set(alltypes).intersection(config.types_not_allowed)) > 0:
                # print("dont include", alltypes, ent.text)
                uentities[ent_text]['is_filtered'] = 1
                uentities[ent_text]['reason_type'] = "not correct type"

            # if uentities[ent_text]['wikipage'] == None:
            #     # print(ent_text,scor,ent.kb_id_,"No wikipage")
            #     uentities[ent_text]['is_filtered'] = 1
            #     uentities[ent_text]['reason_wikipage'] = "No wikipage"

            # print(uentities[ent_text])
        else:
            if ent_text not in uentities:
                print("oh ")
                uentities[entity_concept[ent_text]]['tf'] += 1
            else:
                uentities[ent_text]['tf'] += 1
            # print(uentities[ent_text])

        db_entities = pd.DataFrame.from_dict(uentities, orient='index')

    # if config.debug:
    #     db_entities_filtered = db_entities[db_entities['is_filtered'] == 1]
    #     write_notused(db_entities_filtered)
    db_remain = db_entities[db_entities['is_filtered'] == 0].sort_values(['overall_score'],ascending=False).head(10)
    db_remain['wikipage'] = db_remain['dbpedia_url'].apply(lambda x : get_wikipage(x))
    db_remain = db_remain.reset_index(drop=True)

    return db_remain.to_json(orient='records')


#
# if __name__ == '__main__':
#
#     nlpdb = config.nlpdb
#     EN = config.MODEL_EMBED
#     train_file_path = '/Users/khushboo/Workspace/HELPeR_API/data/test.file.path'
#
#     if config.debug:
#         train_file_path = 'doc_list'
#     train_file_list = []
#     base_path='/Users/khushboo/Workspace/HELPeR_API/'
#     file = open(train_file_path, 'r', encoding='utf8')
#     for line in file:
#
#         text = open(base_path+line.replace("\n", "").strip(), 'r').read()
#         if len(text.strip())  < 10:
#             print("skipping almost empty file ",line)
#             continue
#
#         # if os.path.exists(base_path+line.replace("\n", "") + ".concept.json"):
#         #     continue
#         list_concept, usort = extract_dbpedia(text, nlpdb, EN)
#         fwrite = open(base_path+line.replace("\n", "") + ".concept.json", 'w')
#         for key in usort:
#             fwrite.write(json.dumps(list_concept[key]))
#             fwrite.write("\n")
#         fwrite.close()
#
#         # text_t = preprocessTextMin(text_t,lower=False,stemming=False)
#         # fwrite = open(line.replace("\n", ""), 'w')
#         # fwrite.write(text_t)
#         # fwrite.close()
