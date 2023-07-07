# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
import cv2 #used for image processing and computer vision
import mediapipe as mp #used for ai processing on images and videos
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume #used to access/control volume elements of our system
import numpy as np 

cap = cv2.VideoCapture(0) #caputure video from the camera (0th)

mpHands = mp.solutions.hands  
hands = mpHands.Hands()  #process library to obtain hands
mpDraw = mp.solutions.drawing_utils #to draw stuff on said hands

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume)) #pycaw library fns to access/process audio options of system
 
volMin,volMax = volume.GetVolumeRange()[:2] #get min and max volume provided by pycaw volume pointer

vol=0
volBar=400
volPer=0

while True:   #to keep camera running and perform task continuously
    success,img = cap.read()    #taking camera output 
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) #converting brg colors to rgb
    results = hands.process(imgRGB)

    lmList = []
    if results.multi_hand_landmarks:
        for handlandmark in results.multi_hand_landmarks:
            for id,lm in enumerate(handlandmark.landmark):
                h,w,_ = img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                lmList.append([id,cx,cy]) 
            mpDraw.draw_landmarks(img,handlandmark,mpHands.HAND_CONNECTIONS) #forming lines and points on hand to 
            #get representation of our hand for the program 
    
    if lmList != []:
        x1,y1 = lmList[4][1],lmList[4][2]
        x2,y2 = lmList[8][1],lmList[8][2]  #taking coords of point 4 and 8 as they are finger and thumb

        cv2.circle(img,(x1,y1),8,(0,255,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),8,(0,255,255),cv2.FILLED) #highlighting pts 4 & 8 with differnet coloured points
        cv2.line(img,(x1,y1),(x2,y2),(0,255,255),3)   #forming a line between pts 4 & 8 

        length = hypot(x2-x1,y2-y1) #using hypotnuse fn to find dist. b/w point 4 and 8

        vol = np.interp(length,[20,200],[volMin,volMax]) 
        volBar=np.interp(length,[20,200],[400,150])
        volPer=np.interp(length,[20,200],[0,100]) 
        print(vol,length)
        volume.SetMasterVolumeLevel(vol, None) #setting volume on the basis of length of line

        cv2.rectangle(img,(50,150),(85,400),(112,25,25),3)
        cv2.rectangle(img,(50,int(volBar)),(85,400),(112,25,25),cv2.FILLED) #rectangle for showing volume percentage
        cv2.putText(img,f'{int (volPer)} %',(40,450),cv2.FONT_HERSHEY_TRIPLEX,1,(112,25,25),3) #writing text (%) below rectangle

        # Hand range 20 - 200
        # Volume range -63.5(min) - 0.0(max)
        
    cv2.imshow('Image',img)
    if cv2.waitKey(1) & 0xff==ord('q'):  #to quit enter Q
        break
