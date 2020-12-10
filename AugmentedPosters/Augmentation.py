import cv2
import os
import numpy as np
import time
import sys

URL = "http://192.168.1.2:8080/shot.jpg"
rootdir = "images_db"
targets = []

class Poster:
    def __init__(self, imagePath, score, descriptors):
        self.imagePath = imagePath
        self.score = score
        self.descriptors = descriptors
    def __repr__(self):
        return('Path: ' + self.imagePath + 
               '   Score: ' + self.score)

class Match:
    def __init__(self, poster, matches):
        self.poster = poster
        self.matches = matches
    def __repr__(self):
        return('Poster: ' + self.poster.imagePath)

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
            targets.append(Poster(imagePath, score, descriptors))

#Getting key points and descriptor of target

RetrieveImages()

capture = cv2.VideoCapture(0) # Webcam
orb = cv2.ORB_create(nfeatures = 1000)
sift = cv2.xfeatures2d_SIFT.create()
bf = cv2.BFMatcher()

while True:
    
    #Computer Webcam
    success,imgWebcam = capture.read()
    imgAug = imgWebcam.copy()

    #Phone
    #imgResp = urllib.request.urlopen(URL)
    #imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
    #imgWebcam = cv2.imdecode(imgNp,-1)

    #Detect image from webcam
    kpWebcam, desWebcam = orb.detectAndCompute(imgWebcam, None)
    bestMatch = None

    #Compare webcam image with posters
    for target in targets:
        matches = bf.knnMatch(target.descriptors,desWebcam,k=2)
        good = []

        #Gets matching points
        for m,n in matches:
            if m.distance < 0.75 * n.distance:
                good.append(m)

        if len(good) > 20:
            if(bestMatch is None):
                bestMatch = Match(target, good)
            elif len(good) > len(bestMatch.matches):
                bestMatch = Match(target, good)
                
    cv2.imshow('Webcam', imgWebcam)
    
    # If images have more than 20 matching points
    if bestMatch is not None:

        targetImage = cv2.imread(bestMatch.poster.imagePath)
        kpTarget, desTarget = orb.detectAndCompute(targetImage, None)
        
        # Draws lines between image target and captured image
        imageFeatures = cv2.drawMatches(targetImage, kpTarget, imgWebcam, kpWebcam, bestMatch.matches, None, flags=2)
        cv2.imshow('Images', imageFeatures) 

        targetSrcPoints = np.float32([kpTarget[m.queryIdx].pt for m in bestMatch.matches]).reshape(-1,1,2)
        webcamSrcPoints = np.float32([kpWebcam[m.trainIdx].pt for m in bestMatch.matches]).reshape(-1,1,2)

        matrix, max = cv2.findHomography(targetSrcPoints, webcamSrcPoints, cv2.RANSAC, 5)
        targetHeigth, targetWidth, targetChannel = targetImage.shape

        pts = np.float32([[0,0], [0,targetHeigth - 1], [targetWidth - 1, targetHeigth - 1], [targetWidth - 1, 0]]).reshape(-1,1,2)
        dest = cv2.perspectiveTransform(pts, matrix)
        imageBounds = cv2.polylines(imgWebcam, [np.int32(dest)], True, (255,0,255),3)
        cv2.imshow('ImageBounds',imageBounds)

        mask = np.zeros((imgWebcam.shape[0], imgWebcam.shape[1]), np.uint8)
        cv2.fillPoly(mask, [np.int32(dest)], (255,255,255))
        maskInv = cv2.bitwise_not(mask)
        imgAug = cv2.bitwise_and(imgAug, imgAug, mask = maskInv)

        cv2.putText(imgWebcam, bestMatch.poster.imagePath, (50,50), cv2.FONT_HERSHEY_SIMPLEX , 1, (255,255,255), 2, cv2.LINE_AA)

        cv2.imshow('maskNew', imgAug)

    #cv2.imshow('Features',imgFeatures)
    #cv2.imshow('Image',imgTarget)
    cv2.imshow('Webcam', imgWebcam)

    # 0 - One frame at a time 
    # 1 - Continuous
    cv2.waitKey(1)


