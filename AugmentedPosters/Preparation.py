import sys
import os
import cv2
import numpy as np
import camera_calibration as cam


def createPoster(movieName, classification, imagePath):
    dir = "images_db/" + movieName

        #Check if poster already exists in databases
    if os.path.isdir(dir) is True:
        print("DATABASE: Directory already exists")
        sys.exit()

    #Create directory
    os.makedirs(dir)

    #Create Image
    image = cv2.imread(imagePath)
    cv2.imwrite(dir + '/' + movieName + '_' + classification + '.' + imagePath.split('.')[1] , image)

    #Create features files
    image2 = cv2.imread(dir + '/' + movieName + '_' + classification + '.' + imagePath.split('.')[1])
    sift = cv2.SIFT.create()
    kp, des = sift.detectAndCompute(image2, None)

    #Save descriptors and keypoints in file
    np.save(dir + "/descriptors", des)



def main():
    movieName = sys.argv[1]
    classification = sys.argv[2]
    imagePath = sys.argv[3]

    cam.calibrate()
    createPoster(movieName, classification, imagePath)

    #Show image
    #cv2.imshow('Image', image)
    #cv2.waitKey(0)



if __name__ == "__main__":
    main()
