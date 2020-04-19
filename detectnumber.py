import cv2
import pytesseract

def DetectNumber(Screen, Speed_Region_Y1, Speed_Region_Y2, Speed_Region_X1, Speed_Region_X2, Scale=1):
    
    SpeedImg = Screen[Speed_Region_Y1:Speed_Region_Y2, Speed_Region_X1:Speed_Region_X2]

    SpeedImg = cv2.cvtColor(SpeedImg, cv2.COLOR_RGB2GRAY)

    SpeedImg = cv2.resize(SpeedImg, ((Speed_Region_X2-Speed_Region_X1)*Scale, (Speed_Region_Y2-Speed_Region_Y1)*Scale))

    #SpeedImg = cv2.medianBlur(SpeedImg, 1)

    Speed = pytesseract.image_to_string(SpeedImg, config='-c tessedit_char_whitelist=0123456789')

    return (Speed, SpeedImg)