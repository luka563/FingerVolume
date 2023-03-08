import cv2 as cv
import time
import HandTrackingModule as htm
import math
import numpy as np

### pycaw ###
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

minVolume = volume.GetVolumeRange()[0]
maxVolume = volume.GetVolumeRange()[1]
inc = (maxVolume - minVolume)/100


capture = cv.VideoCapture(0)
wCap, hCap = 640, 480
capture.set(3,wCap)
capture.set(4,hCap)
cTime, pTime = 0, 0
detector = htm.handDetector(detectionCon=0.8)
val = 0
while True:
    success, img = capture.read()
    img = detector.findHands(img,draw = False)

    lmList = detector.findPosition(img,draw=False)
    if len(lmList)!=0:
        x1, y1 = lmList[4][1],lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        middleX, middleY = (x1+x2)//2, (y1+y2)//2

        cv.circle(img, (x1,y1),10,(0,255,0),cv.FILLED)
        cv.circle(img, (x2,y2), 10, (0, 255, 0), cv.FILLED)
        cv.line(img,(x1,y1),(x2,y2),(0,255,0),2)
        cv.circle(img,(middleX,middleY),10, (0, 255, 0), cv.FILLED)
        hypo = math.hypot(x1 - x2, y1 - y2)
        print(hypo)





        if(hypo < 30):
            val = minVolume
            cv.circle(img, (middleX, middleY), 10, (0, 0, 0), cv.FILLED)
        elif(hypo > 230):
            val = maxVolume
        else:
            val = minVolume + inc * ((hypo - 30) / 2)
        volume.SetMasterVolumeLevel(val, None)

    cTime = time.time()
    fps = 1//(cTime-pTime)
    pTime = cTime
    cv.putText(img,f'FPS {int(fps)}',(20,50),cv.FONT_HERSHEY_PLAIN,2,(0,0,255),2)
    cv.imshow("Sound controller", img)
    cv.waitKey(1)