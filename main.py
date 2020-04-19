import numpy as np
import cv2
import time
import pyautogui
import actions
import pytesseract
from grabscreen import grab_screen
from detect import detect
from detectnumber import DetectNumber

"""for i in list(range(4))[::-1]:
    print(i+1)
    time.sleep(1)"""

last_time = time.time()

while True:

    Screen = grab_screen((1280,65,1024,768))
    
    (Speed, SpeedImg) = DetectNumber(Screen,  480,490, 776,795, Scale=1)

    print("Speed: {}".format(Speed))

    cv2.imshow('SpeedImg', SpeedImg)

    #(output_img, bbox, label, conf) = detect(Screen) #object detection
    
    #cv2.imshow('Screen', cv2.resize(output_img, (768,576)))

    """print('Frame took {} seconds'.format(time.time()-last_time))
    last_time = time.time()"""

    
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

