import cv2
import os
import numpy as np
import urllib.request 
import time
import sys

URL = "http://192.168.1.2:8080/shot.jpg"
rootdir = "images_db"
targets = []

class Target:
    def __init__(self, imagePath, score, descriptors):
        self.imagePath = imagePath
        self.score = score
        self.descriptors = descriptors
    def __repr__(self):
        return('Path: ' + self.imagePath + 
               '   Score: ' + self.score)

#Get posters from database
def RetrieveImages():
    for root, dirs, files in os.walk(rootdir):
        for subdir in dirs:
            for root2, dirs2, files2 in os.walk(rootdir + "/" + subdir):
                descriptors = []
                for name in files2:
                    if name == "descriptors.npy":
                        descriptors = np.load(rootdir + '/' + subdir + '/' + name)  
                    else:
                        imagePath = rootdir + '/' + subdir + '/' + name
                        score = name.split('_')[1][0:1]        
            targets.append(Target(imagePath, score, descriptors))

#Getting key points and descriptor of target

RetrieveImages()
capture = cv2.VideoCapture(0) # Webcam
orb = cv2.ORB_create(nfeatures = 1000)
bf = cv2.BFMatcher()

while True:
    
    #Computer Webcam
    success,imgWebcam = capture.read()

    #Phone
    #imgResp = urllib.request.urlopen(URL)
    #imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
    #imgWebcam = cv2.imdecode(imgNp,-1)

    #Detect image from webcam
    kp2, des2 = orb.detectAndCompute(imgWebcam, None)

    #Compare webcam image with posters
    for target in targets:
        matches = bf.knnMatch(target.descriptors,des2,k=2)
        good = []

        #Gets matching points
        for m,n in matches:
            if m.distance < 0.75 * n.distance:
                good.append(m)

        #Number of good matches
        print(len(good))

    #cv2.imshow('Webcam', imgWebcam)
    #cv2.waitKey(0)
    sys.exit()


    
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


