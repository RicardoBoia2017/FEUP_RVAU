import urllib.request 
import cv2
import numpy as np
import time

#IP Webcam url
URL = "http://192.168.1.2:8080/shot.jpg"

while True:    
    imgResp = urllib.request.urlopen(URL)
    imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img = cv2.imdecode(imgNp,-1)
    cv2.imshow('IPWebcam',img)
    q = cv2.waitKey(1) # needed after imshow
    if q == ord("q"):
        break

cv2.DestroyAllWindows()
