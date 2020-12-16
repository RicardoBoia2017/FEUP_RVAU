import sys
import os
import cv2
import numpy as np
import camera_calibration as cam
import util
import db
import argparse

#Store poster and its information
def createPoster(movieName, score, imagePath):
    dir = db.DATABASE_DIR + "/" + movieName

    #Check if poster already exists in databases
    if os.path.isdir(dir) is True:
        print("DATABASE: Directory already exists")
        sys.exit()

    #Create directory
    os.makedirs(dir)

    #New file directory
    new_file_dir = dir + '/' + movieName + '.' + imagePath.split('.')[1]

    #Create Image
    image = cv2.imread(imagePath)
    cv2.imwrite(new_file_dir, image)

    #Create features files
    image2 = cv2.imread(new_file_dir)
    sift = util.sift_create()

    gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)   
    kp, des = sift.detectAndCompute(gray, None)

    #Save descriptors keypoints and score in file
    db.save2json(score, kp, des, db.getDataPath(movieName))

def main():

    #Validate arguments
    parser = argparse.ArgumentParser(description='Prepare setup')
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('--add', '-a', nargs="*", metavar=('path', 'score', 'name'), action='store')
    group.add_argument('--calibrate', '-c', action='store_true')
    group.add_argument('--clean', action='store_true')

    args = parser.parse_args()

    if args.calibrate:
        cam.calibrate()
    
    if args.add:
        if len(sys.argv) < 5:
            print("usage: preparation.py [-+] (--add path score name | --calibrate | --clean)")
            print("preparation.py: error: argument --add/-a: expected at least 3 argument(s)")
            sys.exit()
        path = args.add[0]
        score = args.add[1]
        name = args.add[2]
        for i in range(3, len(sys.argv) - 2):
            name += " " + args.add[i]

        createPoster(name, score, path)

    if args.clean:
        cam.delete()


if __name__ == "__main__":
    main()
