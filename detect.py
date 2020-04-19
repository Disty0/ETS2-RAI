import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox

def detect(screen):
    bbox, label, conf = cv.detect_common_objects(screen)
    output_img = draw_bbox(screen, bbox, label, conf)
    return (output_img ,bbox, label, conf)