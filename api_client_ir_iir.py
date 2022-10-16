import requests
import json, os
import pandas as pd
from blueprints.dbpedia_endpoints.extract_key_localdb import extract_dbpedia
from blueprints.dbpedia_endpoints.key_config import config as config



url = 'http://ngrok.luozm.me:8395/keyphrase/dbpedia_api/dbpedia_ranked_html'
train_file_path = '/Users/khushboo/Downloads/ir_html_update'
exxtra=""
train_file_list = []
base_path = '/Users/khushboo/Workspace/HELPeR_API/'
file = open(train_file_path, 'r', encoding='utf8')
for line in file:
    htmltext = None
    try:
        with open(line.replace("\n", "").strip(), "r", encoding='utf-8') as f:
            htmltext = f.read().encode('utf-8')
            htmltext = str(htmltext)
            htmltext = htmltext.replace("* Robert Mankoff, 0 The New Yorker, 26 January 1998. FINDING OUT ABOUT", " ")
            # htmltext = htmltext.replace(," ")
            # htmltext = htmltext.replace(, " ")
            # htmltext = htmltext.replace(, " ")
        if os.path.exists(line.replace("\n", "") + ".concept.json"+exxtra):
            continue

        if len(htmltext.strip()) < 5:
            print("Skipping almost empty file", line)
            continue
        #results = extract_dbpedia(htmltext,nlpdb=config.nlpdb,EN=config.MODEL_EMBED)
        results=requests.post(url,data=htmltext,timeout=1200)
        fwrite = open( line.replace("\n", "") + ".concept.json"+exxtra, 'w')
        if results != None and results.json() :
            for record in json.loads(results.json()):
                fwrite.write(json.dumps(record) + "\n")

        if results != None and results.json():
            for record in json.loads(results.json()):
                fwrite.write(json.dumps(record) + "\n")
        fwrite.close()
    except:
        print(line)
        print("something went wrong - lets go to the next")




