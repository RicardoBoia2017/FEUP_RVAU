import cv2
import os
import numpy as np
import time
import sys
import camera_calibration as cam
import preparation as prep
import util
import argparse

rootdir = "images_db"
targets = []
TUTORIAL_MODE = False



class Poster:
    def __init__(self, imagePath, movieName, score, kp, descriptors):
        self.movieName = movieName
        self.score = score
        self.kp = kp
        self.descriptors = descriptors
        self.image = cv2.imread(imagePath)

class Match:
    def __init__(self, poster, matches, score):
        self.poster = poster
        self.matches = matches
        self.score = score
    def empty(self):
        return len(self.matches) == 0



#Get posters from database
def retrieveImages():
    for _, dirs, _ in os.walk(rootdir):
        for subdir in dirs:
            for _, _, files2 in os.walk(rootdir + "/" + subdir):
                descriptors = []
                kp = []
                score = 0
                for name in files2:
                    if name == "data.json":
                        score, kp, descriptors = prep.readjson(prep.getDataPath(subdir))
                    else:
                        imagePath = rootdir + '/' + subdir + '/' + name
                        
            targets.append(Poster(imagePath, subdir, score, kp, descriptors))


def getBestMatch(desWebcam):

    bf = cv2.BFMatcher(crossCheck= False)
    bestMatch = Match(None, [], 0)

    #Compare webcam image with posters
    for target in targets:
        matches = bf.knnMatch(target.descriptors,desWebcam,k=2)
        good = []

        #Gets matching points
        for m,n in matches:
            if m.distance < 0.75 * n.distance:
                good.append(m)


        score = 1.0 * len(good)/len(target.descriptors)
        current_score = bestMatch.score

        # print(len(good)/target.descriptors)
        if (len(good) > 20) and (score > current_score):
            bestMatch = Match(target, good, score)
        
    return bestMatch
           


def drawImageBounds(imgWebcam, targetImage, matrix):
    targetHeigth, targetWidth, _ = targetImage.shape
    pts = np.float32([[0,0], [0,targetHeigth - 1], [targetWidth - 1, targetHeigth - 1], [targetWidth - 1, 0]]).reshape(-1,1,2)
    dest = cv2.perspectiveTransform(pts, matrix)
    imageBounds = cv2.polylines(imgWebcam, [np.int32(dest)], True, (255,0,255),3)
    cv2.imshow('ImageBounds',imageBounds)



def writeTitle(imageWebcam,imgWebcam, bestMatch, matrix):

    webcamHeight,webcamWidth,_ = imgWebcam.shape
    blank = np.zeros((webcamHeight,webcamWidth,3), np.uint8)

    (_, textHeight), _ = cv2.getTextSize(bestMatch.poster.movieName, cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
    org = (0, 0 + textHeight)
    cv2.putText(blank, bestMatch.poster.movieName, (org), cv2.FONT_HERSHEY_SIMPLEX , 2, (0,255,0), 2, cv2.LINE_AA)
    blank = cv2.warpPerspective(blank, matrix, (webcamWidth, webcamHeight))

    roi = imgWebcam[0:webcamHeight, 0:webcamWidth]

    img2gray = cv2.cvtColor(blank,cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
    img2_fg = cv2.bitwise_and(blank,blank,mask = mask)

    return cv2.add(img1_bg,img2_fg)


def drawCube(imgWebcam, targetImage, matrix, camera, h):
    targetHeigth, targetWidth, _ = targetImage.shape
    objp = np.zeros((2*2,3), np.float32)
    objp[:,:2] = np.mgrid[0:2,0:2].T.reshape(-1,2)
    
    axis = np.float32([[0,0,0 - h], [0,1,0 - h], [1,1,0 - h], [1,0,0 - h], [0,0,-1 - h], [0,1,-1 - h], [1,1,-1 - h], [1,0,-1 - h]])

    cube_size = min(targetHeigth, targetWidth)/5
    x0 = (targetWidth-cube_size) / 2
    y0 = (targetHeigth-cube_size) / 2
    x1 = x0 + cube_size
    y1 = y0 + cube_size

    pts = np.float32([[x0,y0], [x1, y0], [x0,y1], [x1, y1]]).reshape(-1,1,2)
    dest = cv2.perspectiveTransform(pts, matrix)
    ret,rvecs, tvecs = cv2.solvePnP(objp, dest, camera.mtx, camera.dist)

    if ret == True:
        # project 3D points to image plane
        imgpts, _ = cv2.projectPoints(axis, rvecs, tvecs, camera.mtx, camera.dist)
        
        if not util.isValid(imgpts):  
            imgpts = np.int32(imgpts).reshape(-1,2)

            # draw top layer
            imgWebcam = cv2.drawContours(imgWebcam, [imgpts[4:]],-1,(0,0,0),2)

            # draw bottom layer
            imgWebcam = cv2.drawContours(imgWebcam, [imgpts[:4]],-1,(0,0,0),2)

            # draw sides
            for i,j in zip(range(4),range(4,8)):
                imgWebcam = cv2.line(imgWebcam, tuple(imgpts[i]), tuple(imgpts[j]),(0,0,0),2)



def main():
    camera = cam.Camera() #Load camera calibration file
    retrieveImages() #Load database
    capture = cv2.VideoCapture(0) # Start webcam
    sift = util.sift_create()

    while True:
        
        #Computer Webcam
        _,imgWebcam = capture.read()

        #Process image
        gray = cv2.cvtColor(imgWebcam, cv2.COLOR_BGR2GRAY)
        kpWebcam, desWebcam = sift.detectAndCompute(gray, None)

        if desWebcam is not None:

            #Detect image from webcam
            bestMatch = getBestMatch(desWebcam)

            # If images have more than 20 matching points
            if not bestMatch.empty():

                targetImage = bestMatch.poster.image
                kpTarget = bestMatch.poster.kp
                
                if(TUTORIAL_MODE):
                    # Draws lines between image target and captured image
                    imageFeatures = cv2.drawMatches(targetImage, kpTarget, imgWebcam, kpWebcam, bestMatch.matches, None, flags=2)
                    cv2.imshow('Images', imageFeatures) 


                # Calculate homography
                targetSrcPoints = np.float32([kpTarget[m.queryIdx].pt for m in bestMatch.matches]).reshape(-1,1,2)
                webcamSrcPoints = np.float32([kpWebcam[m.trainIdx].pt for m in bestMatch.matches]).reshape(-1,1,2)
                matrix, _ = cv2.findHomography(targetSrcPoints, webcamSrcPoints, cv2.RANSAC, 5)

                
                if matrix is not None:
                    
                    if(TUTORIAL_MODE):
                        drawImageBounds(imgWebcam, targetImage, matrix)

                    for i in range(bestMatch.poster.score):
                        drawCube(imgWebcam, targetImage, matrix, camera, 1.5*i)

                    imgWebcam = writeTitle(imgWebcam, imgWebcam,bestMatch, matrix)


        cv2.imshow('Webcam', imgWebcam)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--tutorial', '-t', action='store_true')
    args = parser.parse_args()
    
    TUTORIAL_MODE = args.tutorial
    
    main()

