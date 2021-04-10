import requests
import json


url = "http://localhost:5000/teracher/"
data = {
    "name":str("นางสาวปัทมา จีนดี"),
    "username":str("admin"),
    "password":str("1234"),
    
}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
requests.post(url, data=json.dumps(data), headers=headers)

