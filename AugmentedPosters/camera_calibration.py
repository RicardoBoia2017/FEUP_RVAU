import numpy as np
import cv2 as cv
import glob
import json
import os

CHECKERBOARD = (6, 9)  # Define the dimensions of checkerboard 
CALIBRATION_PATH = "calibration/"
CALIBRATION_FILE = "calibration/camera_calibration.json"


def load():
    with open(CALIBRATION_FILE) as f:
        data = json.load(f)
        camera_matrix =  np.array(data["camera_matrix"])
        dist_coeff =  np.array(data["dist_coeff"])


def save(mtx, dist):
    # transform the matrix and distortion coefficients to writable lists
    data = {"camera_matrix": np.asarray(mtx).tolist(), "dist_coeff": np.asarray(dist).tolist()}

    with open(CALIBRATION_FILE, "w") as f:
        json.dump(data, f)


def calibrate():
    if os.path.isfile(CALIBRATION_FILE) is True:
        load()
        print("CALIBRATION: Config file loaded")
    else:
        print("CALIBRATION: Calibrate camera ...")
        ret, mtx, dist = calibrateCamera()
        print("CALIBRATION: RMS - ", ret)
        save(mtx, dist)
        print("CALIBRATION: Config file saved")



def calibrateCamera():

    # termination criteria - accuracy(epsilon) or number of iterations 
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.


    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((CHECKERBOARD[0]*CHECKERBOARD[1],3), np.float32)
    objp[:,:2] = np.mgrid[0:CHECKERBOARD[0],0:CHECKERBOARD[1]].T.reshape(-1,2)
    
    images = glob.glob(CALIBRATION_PATH + '*.jpg')
    
    
    for filename in images:
        img = cv.imread(filename)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv.findChessboardCorners( 
                gray, CHECKERBOARD,  
                cv.CALIB_CB_ADAPTIVE_THRESH  
                + cv.CALIB_CB_FAST_CHECK + 
                cv.CALIB_CB_NORMALIZE_IMAGE)

        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners2)


    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    return ret, mtx, dist


def undistort(img, mtx, dist):

    h,  w = img.shape[:2]
    newcameramtx, roi=cv.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

    # undistort
    dst = cv.undistort(img, mtx, dist, None, newcameramtx)

    # crop the image
    x,y,w,h = roi
    dst = dst[y:y+h, x:x+w]
    return dst



def drawCorners(img, corners2, ret):
    # Draw and display the corners
    cv.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
    cv.imshow('img', img)
    cv.waitKey(0)