import cv2 

def sift_create():
    version = int(cv2.__version__.split('.')[0])
    sift = None
    if version == 3:
        sift = cv2.xfeatures2d.SIFT_create()
    elif version == 4:
        sift = cv2.SIFT.create()
    return sift
