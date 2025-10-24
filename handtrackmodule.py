import cv2
import mediapipe as mp
import time
import math


class handDetector():

    def __init__(self,mode=False,maxHand=2,detectionCon=1,trackCon=0.5):
        self.mode=mode
        self.maxHand=maxHand
        self.detectionCon=detectionCon
        self.trackCon=trackCon


        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(self.mode,self.maxHand,self.detectionCon,self.trackCon)

        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]


    def findHands(self,img,draw=True):

        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        #print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handlms,self.mphands.HAND_CONNECTIONS)

        return img
    
    def finddistance(self,idx1,idx2,img,lmlist,draw=True):
        
        x1,y1=lmlist[idx1][1],lmlist[idx1][2]
        x2,y2=lmlist[idx2][1],lmlist[idx2][2]
        cxx,cyy = (x1+x2)//2,(y1+y2)//2

        lenght = math.hypot(x2-x1,y2-y1)
        
        if draw:
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED)
            cv2.line(img,(x1,y1),(x2,y2),(225,0,255),2)
            cv2.circle(img,(cxx,cyy),15,(0,0,255),cv2.FILLED)

        return lenght
    
    def findPosition(self,img,handNo=0,draw=True):
        bbox=None
        lmlist = []
        if self.results.multi_hand_landmarks:
            myHand=self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myHand.landmark):
                    h,w,c=img.shape
                    cx,cy=int(lm.x * w), int(lm.y * h)
                    #print(id,cx,cy)
                    x_list = []
                    y_list = []
                    for lmm in myHand.landmark:
                        x_list.append(int(lmm.x * w))
                        y_list.append(int(lmm.y * h))
                    lmlist.append([id,cx,cy])
                    x_min, x_max = min(x_list), max(x_list)
                    y_min, y_max = min(y_list), max(y_list)
                    bbox = (x_min,y_min,x_max,y_max)
                    
                    if draw:
                    # Draw rectangle around the whole hand
                        cv2.rectangle(img, (x_min-20, y_min-20), (x_max+20, y_max+20), (0, 255, 0), 2)

                        #cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)

        return lmlist,bbox
    
    def fingersUp(self,lmList):
        fingers = []
        # Thumb
        if lmList[self.tipIds[0]][1] > lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for id in range(1, 5):
            if lmList[self.tipIds[id]][2] < lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

            # totalFingers = fingers.count(1)

        return fingers
    

def main():

    pTime =0
    cTime=0
    cap = cv2.VideoCapture(0)
    detector=handDetector()
    while True:
        success, img = cap.read()    
        img=detector.findHands(img)
        lmlist=detector.findPosition(img)
        if len(lmlist) !=0:
            print(lmlist[4])
        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime

        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,
                    (255,0,255),3)

        cv2.imshow('image',img)
        if (cv2.waitKey(30)==27): 
            break


if __name__== "__main__":
    main()