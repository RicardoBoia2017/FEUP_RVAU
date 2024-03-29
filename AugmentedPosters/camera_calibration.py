import numpy as np
import cv2 as cv
import glob
import json
import os
import sys


CHECKERBOARD = (6, 9)  # Define the dimensions of checkerboard 
CALIBRATION_PATH = "calibration/"
CALIBRATION_FILE = CALIBRATION_PATH + "camera_calibration.json"


class Camera:
    def __init__(self):
        mtx, dist = load()
        self.mtx = mtx
        self.dist = dist

    def undistort(self, img):
        return undistort(img, self.mtx, self.dist)


# Calibration state handler
def calibrate():
    if os.path.isfile(CALIBRATION_FILE) is True:
        print("CALIBRATION: Calibration file already exists")
    else:
        print("CALIBRATION: Calibrate camera ...")
        ret, mtx, dist = calibrateCamera()
        print("CALIBRATION: RMS - ", ret)
        save(mtx, dist)
        print("CALIBRATION: Config file saved")

# Load calibration config 
def load():
    if os.path.isfile(CALIBRATION_FILE) is False:
        print("CALIBRATION: Calibration file missing")
        sys.exit()

    with open(CALIBRATION_FILE) as f:
        data = json.load(f)
        mtx  =  np.array(data["camera_matrix"])
        dist =  np.array(data["dist_coeff"])
        return mtx, dist

# Save calibration config
def save(mtx, dist):
    # transform the matrix and distortion coefficients to writable lists
    data = {"camera_matrix": np.asarray(mtx).tolist(), "dist_coeff": np.asarray(dist).tolist()}

    with open(CALIBRATION_FILE, "w") as f:
        json.dump(data, f)

# Delete calibration file
def delete():
    os.remove(CALIBRATION_FILE)


# Calibrate camera in real time with the webcam
def calibrateCameraLive():
    # termination criteria - accuracy(epsilon) or number of iterations 
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.


    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((CHECKERBOARD[0]*CHECKERBOARD[1],3), np.float32)
    objp[:,:2] = np.mgrid[0:CHECKERBOARD[0],0:CHECKERBOARD[1]].T.reshape(-1,2)
    
    
    capture = cv.VideoCapture(0) # Webcam

    while True:
        _,img = capture.read()
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

            img = cv.drawChessboardCorners(img, (9,6), corners2,ret)
            cv.imshow("img", img)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break


    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    return ret, mtx, dist


# Calibrate camera with the images in calibration folder
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


# Undistort camera image using intrinsic camera parameters
def undistort(img, mtx, dist):
    h,  w = img.shape[:2]
    newcameramtx, roi=cv.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

    # undistort
    dst = cv.undistort(img, mtx, dist, None, newcameramtx)

    # crop the image
    x,y,w,h = roi
    dst = dst[y:y+h, x:x+w]
    return dst