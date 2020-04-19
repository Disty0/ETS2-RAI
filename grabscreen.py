import cv2
import mss
import numpy

def grab_screen(region):
    monitor = {"top": region[1], "left": region[0], "width": region[2], "height": region[3]}
    with mss.mss() as sct:
        img = numpy.array(sct.grab(monitor))
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    return img

