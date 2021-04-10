#!/usr/bin/env python

'''

'''

import cv2
import sys
import os
import utils.lib_commons as lib_commons
ROOT = os.path.dirname(os.path.abspath(__file__))+"/../"
CURR_PATH = os.path.dirname(os.path.abspath(__file__))+"/"
sys.path.append(ROOT)

def par(path):  # Pre-Append ROOT to the path if it's not absolute
    return ROOT + path if (path and path[0] != "/") else path


cfg_all = lib_commons.read_yaml(ROOT + "config/config.yaml")
cfg = cfg_all["s6_test.py"]

CLF=cv2.face.LBPHFaceRecognizer_create()

# CLF.read("classifier.xml")
# FACE_CASCADE=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
CLF.read(str(cfg["face_model"]["classifier"]))
FACE_CASCADE=cv2.CascadeClassifier(str(cfg["face_model"]["haarcascade"]))

class FaceRecognition(object):
    def __init__(self):
        print()      

    def draw_boundary(self,img,classifier,scaleFactor,minNeighbors,color,clf):
        # print("  def draw_boundary \n")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features=classifier.detectMultiScale(gray,scaleFactor,minNeighbors)
        coords=[]
        names="Unknow" 
        name=""
        con=0
        for (x,y,w,h) in features:
            # cv2.rectangle(img,(x,y),(x+w,y+h),color,2)
            id,con= clf.predict(gray[y:y+h,x:x+w])
            # print("  for (x,y,w,h) \n")
            if con <= 100:
                # Add id person
                # print("  if con <= 100 \n")
                if id == 1:
                    name = "Natthawat" 
                if id == 2:
                    name = "Kob"
                if id == 3:
                    name = "Toei"
                if id == 4:
                    name = "Emily Sie"
                # cv2.putText(img,name,(x,y-4),cv2.FONT_HERSHEY_SIMPLEX,0.8,color,2)
            else :
                # print("  else \n")
                name = "Unknow"
                # cv2.putText(img,name,(x,y-4),cv2.FONT_HERSHEY_SIMPLEX,0.8,color,2)

            # names=str(names) +" "+ str(name)

        # conx = "{0}%".format(round(100 - con))
        # print("con %s %.4f"%(conx,con))
        con=con/100
        if name == "":
            name = "Unknow"
            # con = 0
        return name,con


    def detect(self,img,faceCascade,clf):
        # print("  def detect \n")
        name,con=self.draw_boundary(img,faceCascade,1.1,10,(0,0,255),clf)

        return name,con

    def face_ai(self,image):
        # print("  def face_ai \n")
        # cv2.imshow('frame',image)
        name,con=self.detect(image,FACE_CASCADE,CLF)
        # print(" FaceRecognition process :  {}\n".format(str(names)))
        return name,con
