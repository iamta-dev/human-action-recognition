import requests
import json


url = "http://localhost:5000/classRoom/"
data = {
    "className":str("วิชาคณิตศาสตร์ เทอม 2/64"),
    "teacherId":str("1"),
    "time":str("จันทร์ 8:30 - 9:30 น. เเละ ศุกร์ 13:30 - 14:30 น."),
    "roomName":str("ห้อง B203 ตึกรวม 2"),
    "numPerson":str("42"),
    "classLevel":str("ชั้นมัธยมศึกษาปีที่ 4/3"),
    "school":str("โรงเรียนกระบุรีวิทยา"),
    
}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
requests.post(url, data=json.dumps(data), headers=headers)

