import cv2
import numpy as np
import urllib.request 
import time

URL = "http://192.168.1.2:8080/shot.jpg"

def stackImages(imgArray,scale,lables=[]):
    sizeW= imgArray[0][0].shape[1]
    sizeH = imgArray[0][0].shape[0]
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                imgArray[x][y] = cv2.resize(imgArray[x][y], (sizeW,sizeH), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((sizeH, sizeW, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            imgArray[x] = cv2.resize(imgArray[x], (sizeW, sizeH), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        hor_con= np.concatenate(imgArray)
        ver = hor
    if len(lables) != 0:
        eachImgWidth= int(ver.shape[1] / cols)
        eachImgHeight = int(ver.shape[0] / rows)
        print(eachImgHeight)
        for d in range(0, rows):
            for c in range (0,cols):
                cv2.rectangle(ver,(c*eachImgWidth,eachImgHeight*d),(c*eachImgWidth+len(lables[d])*13+27,30+eachImgHeight*d),(255,255,255),cv2.FILLED)
                cv2.putText(ver,lables[d],(eachImgWidth*c+10,eachImgHeight*d+20),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),2)
    return ver

capture = cv2.VideoCapture(0) # Webcam
imgTarget = cv2.imread('drone.jpeg') # Image target

heigth, width, channel = imgTarget.shape # Image dimensions

#Getting key points and descriptor of target

orb = cv2.ORB_create(nfeatures = 1000)
kp1, des1 = orb.detectAndCompute(imgTarget, None)
# imgTarget = cv2.drawKeypoints(imgTarget,kp1,None)

print("Number of matching points")

while True:
    
    #Computer Webcam
    success,imgWebcam = capture.read()

    #Phone
    #imgResp = urllib.request.urlopen(URL)
    #imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
    #imgWebcam = cv2.imdecode(imgNp,-1)

    #imgAug = imgWebcam.copy()
    kp2, des2 = orb.detectAndCompute(imgWebcam, None)
    #imgWebcam = cv2.drawKeypoints(imgWebcam,kp2,None)

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2,k=2)
    good = []

    #Gets matching points
    for m,n in matches:
        if m.distance < 0.75 * n.distance:
            good.append(m)

    print(len(good))

    # Draws lines between image target and captured image
    imgFeatures = cv2.drawMatches(imgTarget, kp1, imgWebcam, kp2, good, None, flags=2)

    # If images have more than 20 matching points
    if len(good) > 20:
        srcPoints = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1,1,2)
        destPoints = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1,1,2)

        matrix, max = cv2.findHomography(srcPoints, destPoints, cv2.RANSAC, 5)

        pts = np.float32([[0,0], [0,heigth], [width, heigth], [width, 0]]).reshape(-1,1,2)
        dest = cv2.perspectiveTransform(pts, matrix)
        img2 = cv2.polylines(imgWebcam, [np.int32(dest)], True, (255,0,255),3)
        #cv2.imshow('ImageBounds',img2)

        imgStacked = stackImages(([imgWebcam,imgTarget],[imgFeatures,img2]),0.5)
        cv2.imshow('Images', imgStacked) 

    #    imgWarp = cv2.warpPerspective(imgVideo, matrix, (imgWebcam.shape[1], imgWebcam.shape[0]))
#
    #    mask = np.zeros((imgWebcam.shape[0], imgWebcam.shape[1]), np.uint8)
    #    cv2.fillPoly(mask, [np.int32(dest)], (255,255,255))
    #    maskInv = cv2.bitwise_not(mask)
    #    imgAug = cv2.bitwise_and(imgAug, imgAug, mask = maskInv)
    #    imgAug = cv2.bitwise_or(imgWarp, imgAug)
#
    #    
    #    cv2.imshow('VideoWrap',imgWarp)
    #    cv2.imshow('maskNew', imgAug)

    #cv2.imshow('Features',imgFeatures)
    #cv2.imshow('Image',imgTarget)
    cv2.imshow('Webcam', imgWebcam)

    # 0 - One frame at a time 
    # 1 - Continuous
    cv2.waitKey(0)


