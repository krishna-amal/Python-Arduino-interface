#!/usr/bin/env python
# coding: utf-8

# In[1]:





# In[ ]:


import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import serial  # add Serial library for Serial communication

Arduino_Serial = serial.Serial('com6', 9600)  # Create Serial port object called arduinoSerialData
# print
Arduino_Serial.readline()  # read the serial data and print it as line
print("pushing data")
from PIL import ImageGrab
 
path = 'ImageBasics'
images = []
classNames = []
nameList = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)
studentname = classNames.copy()
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
 

### FOR CAPTURING SCREEN RATHER THAN WEBCAM
def captureScreen(bbox=(300,300,690+300,530+300)):
    capScr = np.array(ImageGrab.grab(bbox))
    capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
    return capScr
 
encodeListKnown = findEncodings(images)
print('Encoding Complete')
 
cap = cv2.VideoCapture(0)
 
while True:
    success, img = cap.read()
    #img = captureScreen()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
 
    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        #print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex]
            print(name)
            
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            #cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            
            print("distance",faceDis)
            
            distance=round(faceDis[0],2)
            cv2.imshow('Webcam',img)
            if (distance < 0.50):  # if the entered data is 1
            Arduino_Serial.write(str.encode('1'))  # send 1 to arduino
            print("MOTOR IS RUNNING!!!")
            if (distance > 0.50):  # if the entered data is 0
            Arduino_Serial.write(str.encode('2'))  # send 0 to arduino
            print("MOTOR TURNED OFF!!!")
 
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()

