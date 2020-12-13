import cv2
import os
import numpy as np
import time
import sys

rootdir = "images_db"
targets = []

class Poster:
    def __init__(self, imagePath, movieName, score, descriptors):
        self.imagePath = imagePath
        self.movieName = movieName
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
    for _, dirs, _ in os.walk(rootdir):
        for subdir in dirs:
            for _, _, files2 in os.walk(rootdir + "/" + subdir):
                descriptors = []
                for name in files2:
                    if name == "descriptors.npy":
                        descriptors = np.load(rootdir + '/' + subdir + '/' + name)  
                    else:
                        imagePath = rootdir + '/' + subdir + '/' + name
                        score = name.split('_')[1][0:1]        
            targets.append(Poster(imagePath, subdir, score, descriptors))

def writeTitle(imageWebcam, webcamHeight, webcamWidth):
    blank = np.zeros((webcamHeight,webcamWidth,3), np.uint8)

    (_, textHeight), _ = cv2.getTextSize(bestMatch.poster.movieName, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 1)
    org = (0, 0 + textHeight)
    cv2.putText(blank, bestMatch.poster.movieName, (org), cv2.FONT_HERSHEY_SIMPLEX , 0.8, (0,255,0), 1, cv2.LINE_AA)
    blank = cv2.warpPerspective(blank, matrix, (webcamWidth, webcamHeight))

    roi = imgWebcam[0:webcamHeight, 0:webcamWidth]

    img2gray = cv2.cvtColor(blank,cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)

    img2_fg = cv2.bitwise_and(blank,blank,mask = mask)

    return cv2.add(img1_bg,img2_fg)    

RetrieveImages()
capture = cv2.VideoCapture(0) # Webcam
orb = cv2.ORB_create(nfeatures = 1000)
sift = cv2.xfeatures2d_SIFT.create()
bf = cv2.BFMatcher()

while True:
    
    #Computer Webcam
    success,imgWebcam = capture.read()
    imgAug = imgWebcam.copy()

    #Detect image from webcam
    kpWebcam, desWebcam = sift.detectAndCompute(imgWebcam, None)
    bestMatch = None

    #Compare webcam image with posters
    for target in targets:
        matches = bf.knnMatch(target.descriptors,desWebcam,k=2)
        good = []

        #Gets matching points
        for m,n in matches:
            if m.distance < 0.75 * n.distance:
                good.append(m)

        print(len(good))

        if len(good) > 20:
            if(bestMatch is None):
                bestMatch = Match(target, good)
            elif len(good) > len(bestMatch.matches):
                bestMatch = Match(target, good)
                
    cv2.imshow('Webcam', imgWebcam)
    
    # If images have more than 20 matching points
    if bestMatch is not None:

        targetImage = cv2.imread(bestMatch.poster.imagePath)
        kpTarget, desTarget = sift.detectAndCompute(targetImage, None)
        
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

        webcamHeight,webcamWidth,WebcamChannels = imgWebcam.shape
        title = writeTitle(imgWebcam, webcamHeight, webcamWidth)

        imgWebcam[0:webcamHeight, 0:webcamWidth ] = title

        cv2.imshow('maskNew', imgAug)

    #cv2.imshow('Features',imgFeatures)
    #cv2.imshow('Image',imgTarget)
    cv2.imshow('Webcam', imgWebcam)

    # 0 - One frame at a time 
    # 1 - Continuous
    cv2.waitKey(1)


