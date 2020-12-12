import cv2
import os
import numpy as np
import time
import sys

URL = "http://192.168.1.2:8080/shot.jpg"
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
            targets.append(Poster(imagePath, subdir, score, descriptors))

#Getting key points and descriptor of target

RetrieveImages()
#drone = cv2.imread("drone.jpeg")#
#rows,cols,channels = drone.shape
#blank = np.zeros((rows,cols,3), np.uint8)
#
#cv2.putText(blank, "example", (0,50), cv2.FONT_HERSHEY_SIMPLEX , 0.6, (0,255,0), 1, cv2.LINE_AA)
#
#roi = drone[0:rows, 0:cols ]
#
#img2gray = cv2.cvtColor(blank,cv2.COLOR_BGR2GRAY)
#ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
#mask_inv = cv2.bitwise_not(mask)
#
#img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
#
#img2_fg = cv2.bitwise_and(blank,blank,mask = mask)
#
#dst = cv2.add(img1_bg,img2_fg)
#drone[0:rows, 0:cols ] = dst



#rgba = cv2.cvtColor(blankImage, cv2.COLOR_RGB2RGBA)
#angle = 30
#rgba[:, :, 3] = 0
#blankImage[:, :, 2] = 255
#cv2.putText(rgba, "example", (100,100), cv2.FONT_HERSHEY_SIMPLEX , 1, (255,255,255), 1, cv2.LINE_AA)
#M = cv2.getRotationMatrix2D((100,100), angle, 1)
#out = cv2.warpAffine(rgba, M, (rgba.shape[1], rgba.shape[0]))
#cv2.imshow("Transparent", rgba)
##res = cv2.bitwise_and(blankImage,blankImage, mask= rgba)
#cv2.imshow("OG",blankImage)
#cv2.imshow("Res",out)

#cv2.imshow("Transparent",rgba)
#cv2.imwrite("transparent.png" , rgba)

#cv2.waitKey(0)
#sys.exit()

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

        #mask = np.zeros((imgWebcam.shape[0], imgWebcam.shape[1]), np.uint8)
        #cv2.fillPoly(mask, [np.int32(dest)], (255,255,255))
        #maskInv = cv2.bitwise_not(mask)
        #imgAug = cv2.bitwise_and(imgAug, imgAug, mask = maskInv)

        webcamHeight,webcamWidth,WebcamChannels = imgWebcam.shape
        blank = np.zeros((webcamHeight,webcamWidth,3), np.uint8)

        (textWidth, textHeight), baseline = cv2.getTextSize(bestMatch.poster.movieName, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 1)
        org = (0, 0 + textHeight)
        cv2.putText(blank, bestMatch.poster.movieName, (org), cv2.FONT_HERSHEY_SIMPLEX , 0.8, (0,255,0), 1, cv2.LINE_AA)
        blank = cv2.warpPerspective(blank, matrix, (webcamWidth, webcamHeight))

        roi = imgWebcam[0:webcamHeight, 0:webcamWidth]

        img2gray = cv2.cvtColor(blank,cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)

        img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)

        img2_fg = cv2.bitwise_and(blank,blank,mask = mask)

        dst = cv2.add(img1_bg,img2_fg)
        imgWebcam[0:webcamHeight, 0:webcamWidth ] = dst

        cv2.imshow('maskNew', imgAug)

    #cv2.imshow('Features',imgFeatures)
    #cv2.imshow('Image',imgTarget)
    cv2.imshow('Webcam', imgWebcam)

    # 0 - One frame at a time 
    # 1 - Continuous
    cv2.waitKey(0)


