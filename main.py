import numpy as np
import cv2
import time
from grabscreen import grab_screen
import detect
import pyautogui
import actions
import pytesseract

"""for i in list(range(4))[::-1]:
    print(i+1)
    time.sleep(1)"""

last_time = time.time()

while True:

    Screen = grab_screen((1280,65,1024,768))
    #(output_img, bbox, label, conf) = detect.detect(screen) #object detection

    SpeedImg = Screen[480:490, 776:795]
    WayPointDistanceImg = Screen[603:612, 842:860]

    SpeedImg = cv2.cvtColor(SpeedImg, cv2.COLOR_RGB2GRAY)
    WayPointDistanceImg = cv2.cvtColor(WayPointDistanceImg, cv2.COLOR_RGB2GRAY)

    """SpeedImg = cv2.resize(SpeedImg, (304,80))
    WayPointDistanceImg = cv2.resize(WayPointDistanceImg, (288,162))"""

    """SpeedImg = cv2.medianBlur(SpeedImg, 1)
    WayPointDistanceImg = cv2.medianBlur(WayPointDistanceImg, 1)"""

    Speed = pytesseract.image_to_string(SpeedImg, config='-c tessedit_char_whitelist=0123456789')
    WayPointDistance = pytesseract.image_to_string(WayPointDistanceImg, config='-c tessedit_char_whitelist=0123456789')

    print("Speed: {} , Distance: {}".format(Speed, WayPointDistance))

    #print('Frame took {} seconds'.format(time.time()-last_time))
    #last_time = time.time()
    cv2.imshow('window', WayPointDistanceImg) #cv2.resize(screen, (768,576))
    cv2.imshow('speed', SpeedImg)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

