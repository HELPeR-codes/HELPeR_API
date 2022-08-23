from SPARQLWrapper import SPARQLWrapper, JSON
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from sentence_transformers import util
import json
import html2text
import os
import unicodedata
import re
from blueprints.dbpedia_endpoints.key_config import  config
def remove_html_from_text(htmltext):

    data = config.h.handle(htmltext)
    data = data.replace("Online edition c Cambridge UP"," ")
    data = data.replace("DRAFT April Cambridge University Press Feedback welcome"," ")
    data = preprocessText(data)
    data = data.replace("Online edition c Cambridge UP"," ")
    data = data.replace("DRAFT April Cambridge University Press Feedback welcome"," ")
    data = data.replace("ﬁ","fi")
    data = data.replace("ﬂ", "fl")
    data_noenglish = re.sub("[a-zA-Z0-9]+", "",data).strip()

    if len(data_noenglish) > 0:
        print(data_noenglish)

    return data

def remove_html(filename):
    htmltext = None
    with open(filename.replace("\n", "").strip(), "r", encoding='utf-8') as f:
        htmltext = f.read()

    # text = open(line.replace("\n", "").strip(), 'r').read()

    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_tables = True
    h.ignore_images = True
    h.ignore_emphasis = True
    h.body_width = 10000
    data = h.handle(htmltext)
    data = data.replace("Online edition c Cambridge UP"," ")
    data = data.replace("DRAFT April Cambridge University Press Feedback welcome"," ")
    data = preprocessText(data)
    data = data.replace("Online edition c Cambridge UP"," ")
    data = data.replace("DRAFT April Cambridge University Press Feedback welcome"," ")
    data = data.replace("ﬁ","fi")
    data = data.replace("ﬂ", "fl")
    data_noenglish = re.sub("[a-zA-Z0-9]+", "",data).strip()

    if len(data_noenglish) > 0:
        print(data_noenglish)
        print("problem")

    fwrite = open(filename.replace("\n", "").strip()+".txt",'w')

    fwrite.write(data)
    return data

def preprocessText(text, stemming=False, lower=False):
    text = text.replace("\n", "")
    text = re.sub("[ ]{1,}", r' ', text)

    text = re.sub(r'\W+|\d+', ' ', text.strip())
    if lower:
        text = text.lower()

    tokens = word_tokenize(text)
    tokens = [token.strip() for token in tokens]
    # fwrite = open("pre-processed_file.txt", 'w')
    # fwrite.write(" ".join(tokens))
    return " ".join(tokens)



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
prefix dbpedia-owl: <http://dbpedia.org/ontology/>
SELECT DISTINCT ?obj WHERE{
<{@url}>  dbpedia-owl:abstract  ?obj
filter(langMatches(lang(?obj),"en"))
} limit 1
    '''.replace('{@url}',url)

    sparql.setQuery(query)  # the previous query as a literal string
    a = sparql.query().convert()
    description = url.split("/")[-1]
    if a is not None:
        if a['results']['bindings'][0]['obj']['value'] is not None:
            description = ' '.join(a['results']['bindings'][0]['obj']['value'].split(" ")[0:50])

    return description


import threading
import requests
sem = threading.Semaphore()

def get_wikipage(url):
    wikipage=None
    data = requests.get(url.replace("/resource/", "/data/") + ".json").json()
    dbpedia_json = data[url]

    if 'http://xmlns.com/foaf/0.1/isPrimaryTopicOf' in dbpedia_json:
        wikipage = dbpedia_json['http://xmlns.com/foaf/0.1/isPrimaryTopicOf'][0]['value']
    return wikipage

def write_notused(db):
    while True:
        sem.acquire()
        config.f_notusedwriter.write(db.to_json(orient='records',lines=True))
        sem.release()