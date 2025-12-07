
import json
import requests
    

def send(url,data):
        data = {"content" :  data}
        requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
