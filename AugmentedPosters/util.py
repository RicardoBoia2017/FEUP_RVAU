import cv2 

#Create SIFT objecgt according to Python version
def sift_create():
    version = int(cv2.__version__.split('.')[0])
    sift = None
    if version == 3:
        sift = cv2.xfeatures2d.SIFT_create(nfeatures = 1000)
    elif version == 4:
        sift = cv2.SIFT.create(nfeatures = 1000)
    return sift

#Check if points are valid
def isValid(pts):
    return any(x<0 for x in pts.reshape(-1))