import json, requests

while(1):
    url = requests.get("172.16.0.1/FieldData/GetData")
    data = json.loads(url.text)
    print data
