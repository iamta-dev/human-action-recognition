import requests
import json
from datetime import datetime

# url = "http://localhost:5000/human-action/"
# data = {
#     "dateTime":"28/01/21 02:46:42",
#     "face":"Natthawat",
#     "face_acc":"96.32%",
#     "action":"sleeping",
#     "action_acc":"84.65%",
#     "position":"345,567,45,789"
# }
# headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
# r = requests.post(url, data=json.dumps(data), headers=headers)
# reading
# writing
# raiseHand
# sleeping
# standing
# siting


class Task():
    def postData(self):
        classId = "1" 
        face = "Natthawat"
        face_acc = "94%"
        action = "siting"
        action_acc = "99%"
        position = "850,441"
        self.postHumanAction(classId,face,face_acc,action,action_acc,position)
        return 0

    def postHumanAction(self,classId,face,face_acc,action,action_acc,position):
            now = datetime.now()
            # dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            dt_string = "11-03-2021 15:40:34"
            # print(dt_string)
            url = "http://localhost:5000/human-action/"
            data = {
                "classId":str(classId),
                "dateTime":str(dt_string),
                "face":str(face),
                "face_acc":str(face_acc),
                "action":str(action),
                "action_acc":str(action_acc),
                "position":str(position),
            }
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            requests.post(url, data=json.dumps(data), headers=headers)


obj = Task()
obj.postData()