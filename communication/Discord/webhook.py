
import json
import requests
    

def send(url,infos,polling = 5):
        data = {"embeds": [{"fields": [], "color": 16711680}]}
        if type(infos) == dict : 
                for key in infos.keys() : 
                        data["embeds"][0]["fields"].append({"name": key, "value": infos[key], "inline": True})
        else : 
                data["embeds"][0]["fields"].append({"name": "Information", "value": str(infos), "inline": False})

        state = False
        for _ in range(polling):
                if state :
                        break
                try : 
                        requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
                        state = True
                except : 
                        pass
