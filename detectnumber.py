import cv2
import pytesseract
import numpy as np

def DetectNumber(Screen, Speed_Region_Y1, Speed_Region_Y2, Speed_Region_X1, Speed_Region_X2): #Scale=1
    
    SpeedImg = Screen[Speed_Region_Y1:Speed_Region_Y2, Speed_Region_X1:Speed_Region_X2]

    SpeedImg = cv2.cvtColor(SpeedImg, cv2.COLOR_RGB2GRAY)

    SpeedImg = cv2.resize(SpeedImg,None,fx=3,fy=2,interpolation=cv2.INTER_LINEAR) 

    Speed = pytesseract.image_to_string(SpeedImg, config='load_freq_dawg = False load_system_dawg = False -c tessedit_char_whitelist=0123456789')

    return (Speed, SpeedImg)