import cv2
from handtrackmodule import handDetector
import time 
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = handDetector()
finalText = ''

keyboard = Controller()

# Updated keyboard layout
keys = [
    ['Q','W','E','R','T','Y','U','I','O','P','<-'],
    ['A','S','D','F','G','H','J','K','L',';'],
    ['Z','X','C','V','B','N','M',',','.','/']
]

class Button():
    def __init__(self,pos,text,size=[85,85]):
        self.pos = pos
        self.text = text
        self.size = size

def drawButton(img,button,hover=False,click=False):
    x,y = button.pos
    w,h = button.size
    
    # Base button color
    if click:
        color = (255,255,255)
        text_color = (0,0,0)
    elif hover:
        color = (100,100,255)
        text_color = (255,255,255)
    else:
        color = (50,50,50)
        text_color = (255,255,255)
    
    # Draw rounded rectangle style
    cv2.rectangle(img,(x,y),(x+w,y+h),color,-1,cv2.LINE_AA)
    cv2.rectangle(img,(x,y),(x+w,y+h),(200,200,200),2,cv2.LINE_AA)
    
    # Center text
    font_scale = 2 if button.text not in ["SPACE","<-"] else 2
    (tw,th), _ = cv2.getTextSize(button.text,cv2.FONT_HERSHEY_PLAIN,font_scale,2)
    cx, cy = x + (w - tw)//2, y + (h + th)//2
    cv2.putText(img,button.text,(cx,cy),cv2.FONT_HERSHEY_PLAIN,font_scale,text_color,2)

def drawAll(img,ButtonList):
    for button in ButtonList:
        drawButton(img,button)
    return img


ButtonList = []
start_x = 50
start_y = 50
key_w, key_h = 85, 85
spacing = 10

# Build QWERTY rows
for i,row in enumerate(keys):
    row_offset = i * (key_h + spacing)
    for j,key in enumerate(row):
        # Shift rows like real keyboard
        offset_x = 0
        if i == 1: offset_x = 45
        if i == 2: offset_x = 90

        size = [key_w, key_h]
        if key == "<-":
            size = [170, key_h]   # Wider backspace key
        ButtonList.append(Button([start_x + j*(key_w+spacing) + offset_x, start_y+row_offset], key, size))

# Add SPACE bar just below alphabets
space_y = start_y + 3*(key_h + spacing) + 20
ButtonList.append(Button([start_x+200, space_y], "SPACE", [500,85]))


while True:
    success,img = cap.read()
    img = cv2.flip(img,1)
    img = detector.findHands(img)
    lmlist,bbox = detector.findPosition(img)

    img = drawAll(img,ButtonList)

    if lmlist:
        for button in ButtonList:
            x,y = button.pos
            w,h = button.size
            if x<lmlist[8][1]<x+w and y<lmlist[8][2]<y+h:
                # Hover effect
                drawButton(img,button,hover=True)

                length = detector.finddistance(8,12,img,lmlist,False)
                print(length)
                
                if length<50:
                    # Click effect
                    drawButton(img,button,click=True)

                    if button.text == "SPACE":
                        keyboard.press(' ')
                        finalText += ' '
                    elif button.text == "<-":
                        finalText = finalText[:-1]
                    else:
                        keyboard.press(button.text)
                        finalText += button.text
                    time.sleep(0.2)
    
    # Text area
    cv2.rectangle(img,(50,600),(1100,700),(255,255,255),cv2.FILLED)
    cv2.putText(img,finalText,(60,680),cv2.FONT_HERSHEY_PLAIN,4,(0,0,0),4)

    cv2.imshow('Virtual Keyboard',img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
