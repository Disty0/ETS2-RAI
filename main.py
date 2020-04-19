import numpy as np
import cv2
import time
from grabscreen import grab_screen
import detect
import pyautogui
import actions
import pytesseract
import detectnumber

"""for i in list(range(4))[::-1]:
    print(i+1)
    time.sleep(1)"""

last_time = time.time()

while True:

    Screen = grab_screen((1280,65,1024,768))
    #(output_img, bbox, label, conf) = detect.detect(screen) #object detection

    (Speed, SpeedImg) = detectnumber.DetectNumber(Screen,  480,490, 776,795, Scale=1)

    print("Speed: {}".format(Speed))

    #print('Frame took {} seconds'.format(time.time()-last_time))
    #last_time = time.time()

    #cv2.imshow('Screen', cv2.resize(Screen, (768,576)))

    cv2.imshow('SpeedImg', SpeedImg)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

