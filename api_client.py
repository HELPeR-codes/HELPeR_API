import requests
import pandas as pd
file_data = "I hope you get well soon. I also went through the same process of chemo ".encode('utf-8')
# response = requests.post("http://ngrok.luozm.me:8395/keyphrase/annotation_api/updates",data='01-01-2020')
# # response = requests.post("http://localhost:10081/basic_api/role", data=file_data)
# df = pd.DataFrame(response.json())

url = 'http://ngrok.luozm.me:8395/keyphrase/recsys_api/rec'

data = {'userid': '1', 'kw': '[1,2,3]', 'utype': '["patient","caregiver","patient and caregiver","Health professional"]',
     'query': "hair loss and pain during chemotherapy"}

#params = {'sessionKey': '9ebbd0b25760557393a43064a92bae539d962103', 'format': 'xml', 'platformId': 1}

response = requests.post(url, json=data)
print(response)
