import requests
import json
import os

# url = 'http://ngrok.luozm.me:8395/keyphrase/dbpedia_api/dbpedia_ranked'

# files forwhich concepts are to be extracted - assumed to be in text format
#keep absolute path if necessary
# train_file_path = '/Users/khushboo/Workspace/HELPeR_API/data/test.file.path'
#
# train_file_list = []
# file = open(train_file_path, 'r', encoding='utf8')
#
# # for each file generate concepts and write in a json file
# for line in file:
#     text = open( line.replace("\n", "").strip(), 'r').read().encode('utf-8')
#     print(len(text.split()))
#     if len(text.strip()) < 10:
#         print("skipping almost empty file ", line)
#         continue
#     print("filename", line)
#
#     if os.path.exists(line.replace("\n", "") + ".concept.json"):
#         continue
#     results = requests.post(url,data=text,timeout=500)
#
#     fwrite = open( line.replace("\n", "") + ".concept.json", 'w')
#     for record in json.loads(results.json()):
#         fwrite.write(json.dumps(record) + "\n")
#     fwrite.close()

url = 'http://ngrok.luozm.me:8395/keyphrase/recsys_api/rec'
# url = 'http://127.0.0.1:10087/dbpedia_api/dbpedia_ranked'

data = {'userid': '1', 'kw': '[1,2,3]', 'utype': '["patient","caregiver","patient and caregiver","Health professional"]',
     'query': "hair loss and pain during chemotherapy"}

headers = {'Content-Type': 'application/json'}
import time
now1 = time.time()
response = requests.post(url, headers=headers,json=json.dumps(data))
now2 = time.time() - now1
print(response.json())


print(now2)
data = {'userid': '1', 'kw': '[1,2,3]', 'utype': '["patient","caregiver","patient and caregiver"]'
     }

headers = {'Content-Type': 'application/json'}
now1 = time.time()
response = requests.post(url, headers=headers,json=json.dumps(data))
now2 = time.time() - now1
print(now2)
print(response.json())

