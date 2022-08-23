import re
from nltk.tokenize import sent_tokenize, word_tokenize
from sentence_transformers import util
print("load model")
import requests
# initialize language model
from blueprints.dbpedia_endpoints.key_config import config
import operator
from SPARQLWrapper import SPARQLWrapper, JSON


def preprocessText(text, stemming=False, lower=False):
    text = text.replace("\n", " ")
    text = re.sub("[ ]{1,}", r' ', text)

    text = re.sub(r'\W+|\d+', ' ', text.strip())
    if lower:
        text = text.lower()

    tokens = word_tokenize(text)
    tokens = [token.strip() for token in tokens]
    # fwrite = open("pre-processed_file.txt", 'w')
    # fwrite.write(" ".join(tokens))
    return " ".join(tokens)


# # load your model as usual
# # nlp = spacy.load('en_core_web_lg')
# # # add the pipeline stage
# # nlp.add_pipe('dbpedia_spotlight')
# # # get the document
# # doc = nlp('The president of USA is calling Boris Johnson to decide what to do about coronavirus')
#
# # import spacy_dbpedia_spotlight
# # import spacy
# # nlp = spacy.load("en_core_web_sm")
# # nlpdb = spacy.blank('en')
#
import spacy_dbpedia_spotlight

# nlpdb = spacy_dbpedia_spotlight.create('en')
# add the pipeline stage
#nlpdb.add_pipe('dbpedia_spotlight')
# from config import config


# bc =  BertClient(port=5555, port_out=5556, check_version=False)
import numpy as np
import math


# from embedding_as_service.text.encode import Encoder
# en = Encoder(embedding='bert', model='bert_base_cased', max_seq_length=256)

def scoring(pair, EN):
    # vecs =
    query_vec_1 = EN.encode(pair[0])
    query_vec_2 = EN.encode(pair[1])
    sim = round(util.pytorch_cos_sim(query_vec_1, query_vec_2).item(), 5)
    return sim


def get_type(url):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)
    query ='''
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbr: <http://dbpedia.org/resource>
PREFIX dbo: <http://dbpedia.org/ontology>
SELECT DISTINCT ?obj WHERE{
<{@url}>  rdf:type ?obj
FILTER strstarts(str(?obj), str(dbo:))}
    '''.replace('{@url}',url)

#     """
#     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#     SELECT ?type
#     WHERE { <http://dbpedia.org/resource/Donald_Broadbent> rdfs:type ?type }
# """
    sparql.setQuery(query)  # the previous query as a literal string

    return sparql.query().convert()

def get_abstract(url):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)
    query ='''
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbr: <http://dbpedia.org/resource>
PREFIX dbo: <http://dbpedia.org/ontology>
SELECT DISTINCT ?obj WHERE{
<{@url}>  rdf:comment ?obj
FILTER strstarts(str(?obj), str(dbo:))}
    '''.replace('{@url}',url)

#     """
#     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#     SELECT ?type
#     WHERE { <http://dbpedia.org/resource/Donald_Broadbent> rdfs:type ?type }
# """
    sparql.setQuery(query)  # the previous query as a literal string

    return sparql.query().convert()

types_not_allowed = set([ 'Place', 'Species', 'Event','Person','Agent'])
from random import seed
from random import randint

import time
def extract_dbpedia(text, nlpdb, EN):
    # print(text)
    text = preprocessText(text,lower=False,stemming=False)
    doc = nlpdb(text)
    uentities = {}
    minsc = +1
    maxsc = -1
    dbpedia_page = []
    dbpedia_page_not_selected=[]
    for ent in doc.ents:
        dup = 0
        alltypes = []
        wikipage = None

        ent_text = ent.text.lower()
        if ent.kb_id_ is None or ent.kb_id_ == "":
            print(ent.text, "not dbpedia - so ignored")
            continue



        if ent_text not in uentities:
            if ent.kb_id_ in dbpedia_page:
                print("duplicate entity", ent.kb_id_)
                dup = 1
                continue

            scor = scoring([ent.text, text], EN)

            if scor < 0.7:
                print(ent_text,scor,ent.kb_id_,"removed because of low score")
                continue

            minsc = min(minsc, scor)
            maxsc = max(maxsc, scor)
            linkscore = 1
            if ent and ent._.dbpedia_raw_result and ent._.dbpedia_raw_result['@similarityScore']:
                linkscore = float(ent._.dbpedia_raw_result['@similarityScore'])
            if linkscore < 0.85:
                print(ent_text, linkscore, ent.kb_id_,"removed because of low links score")
                continue

            type = 'unknown'
            if ent and ent._.dbpedia_raw_result and ent._.dbpedia_raw_result['@types']:
                abc = ent._.dbpedia_raw_result['@types'].split(",")
                for x in abc:
                    if "DBpedia:" in x:
                        alltypes.append(x.split("DBpedia:")[1])

            a = get_type(ent.kb_id_)
            if a is not None:
                for obj in a['results']['bindings']:
                    alltypes.append(obj['obj']['value'].split("/")[-1])



            if len(set(alltypes).intersection(types_not_allowed)) > 0:
                print("dont include", alltypes, ent.text)
                continue



            # print(ent_text,alltypes)
            if ent.kb_id_ is not None and "dbpedia" in ent.kb_id_:
                data = requests.get(ent.kb_id_.replace("/resource/", "/data/") + ".json").json()
                dbpedia_json = data[ent.kb_id_]
                if 'http://xmlns.com/foaf/0.1/isPrimaryTopicOf' in dbpedia_json:
                    wikipage = dbpedia_json['http://xmlns.com/foaf/0.1/isPrimaryTopicOf'][0]['value']
                    # print(wikipage)

            dbpedia_page.append(ent.kb_id_)

            uentities[ent_text] = {'concept': ent.text,
                                   'tf': 1,
                                   'dbpedia_url': ent.kb_id_,
                                   'wikpage': wikipage,
                                   'link_score': ent._.dbpedia_raw_result['@similarityScore'],
                                   'types': alltypes,
                                   # 'support': ent._.dbpedia_raw_result['@support'],
                                   'score': scor,
                                   'is_repeated': dup
                                   }
            # print(uentities[ent_text])
        else:
            uentities[ent_text]['tf'] += 1
            # print(uentities[ent_text])
    # if 'foo' in doc.spans:
    #     for ent in doc.spans['foo']:
    #         dup = 0
    #         alltypes = []
    #         wikipage = None
    #
    #         ent_text = ent.text.lower()
    #         if ent.kb_id_ is None or ent.kb_id_ == "":
    #             print(ent.text, "not dbpedia - so ignored")
    #             continue
    #
    #         if ent_text not in uentities:
    #             if ent.kb_id_ in dbpedia_page:
    #                 print("duplicate entity", ent.kb_id_)
    #                 dup = 1
    #
    #             scor = scoring([ent.text.lower(), text.lower()], EN)
    #             minsc = min(minsc, scor)
    #             maxsc = max(maxsc, scor)
    #             linkscore = 1
    #             if ent and ent._.dbpedia_raw_result and ent._.dbpedia_raw_result['@similarityScore']:
    #                 linkscore = float(ent._.dbpedia_raw_result['@similarityScore'])
    #             if linkscore < 0.9:
    #                 print(ent_text, linkscore, ent.kb_id_)
    #                 continue
    #
    #             type = 'unknown'
    #             if ent and ent._.dbpedia_raw_result and ent._.dbpedia_raw_result['@types']:
    #                 abc = ent._.dbpedia_raw_result['@types'].split(",")
    #                 for x in abc:
    #                     if "DBpedia:" in x:
    #                         alltypes.append(x.split("DBpedia:")[1])
    #
    #             if len(set(alltypes).intersection(types_not_allowed)) > 0:
    #                 print("dont include", alltypes, ent.text)
    #                 continue
    #                 print("include",ent.text)
    #             # print(ent_text,alltypes)
    #             if ent.kb_id_ is not None and "dbpedia" in ent.kb_id_:
    #                 data = requests.get(ent.kb_id_.replace("/resource/", "/data/") + ".json").json()
    #                 dbpedia_json = data[ent.kb_id_]
    #                 if 'http://xmlns.com/foaf/0.1/isPrimaryTopicOf' in dbpedia_json:
    #                     wikipage = dbpedia_json['http://xmlns.com/foaf/0.1/isPrimaryTopicOf'][0]['value']
    #                     # print(wikipage)
    #
    #             dbpedia_page.append(ent.kb_id_)
    #
    #             uentities[ent_text] = {'concept': ent.text,
    #                                    'tf': 1,
    #                                    'dbpedia_url': ent.kb_id_,
    #                                    'wikpage': wikipage,
    #                                    # 'link_score': ent._.dbpedia_raw_result['@similarityScore'],
    #                                    'types': alltypes,
    #                                    # 'support': ent._.dbpedia_raw_result['@support'],
    #                                    'score': scor,
    #                                    'is_repeated': dup
    #                                    }
    #             # print(uentities[ent_text])
    #         else:
    #             uentities[ent_text]['tf'] += 1
    #             # print(uentities[ent_text])

    print(minsc, maxsc)
    maxsc = minsc + 0.000000001
    minsc = minsc - 0.00000001

    usort = {}
    for key in uentities:
        # nscore = round((uentities[key]['score'] * uentities[key]['tf'] - minsc) / (maxsc - minsc), 10)
        usort[key] = min(1, uentities[key]['score'])
        # uentities[key]['nscore'] = nscore

    usort1 = dict(sorted(usort.items(), key=operator.itemgetter(1), reverse=True))

    return uentities, usort1


import json

import os

if __name__ == '__main__':

    nlpdb = config.nlpdb
    EN = config.MODEL_EMBED
    train_file_path = '/Users/khushboo/Workspace/HELPeR_API/data/test.file.path'

    if config.debug:
        train_file_path = 'doc_list'
    train_file_list = []
    base_path='/Users/khushboo/Workspace/HELPeR_API/'
    file = open(train_file_path, 'r', encoding='utf8')
    for line in file:

        text = open(base_path+line.replace("\n", "").strip(), 'r').read()
        if len(text.strip())  < 10:
            print("skipping almost empty file ",line)
            continue

        if os.path.exists(base_path+line.replace("\n", "") + ".concept.json"):
            continue
        list_concept, usort = extract_dbpedia(text, nlpdb, EN)
        fwrite = open(base_path+line.replace("\n", "") + ".concept.json", 'w')
        for key in usort:
            fwrite.write(json.dumps(list_concept[key]))
            fwrite.write("\n")
        fwrite.close()

        # text_t = preprocessTextMin(text_t,lower=False,stemming=False)
        # fwrite = open(line.replace("\n", ""), 'w')
        # fwrite.write(text_t)
        # fwrite.close()
