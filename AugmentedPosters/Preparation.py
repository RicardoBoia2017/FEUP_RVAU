import sys
import os
import cv2
import numpy as np
import camera_calibration as cam

import json

DATABASE_DIR = "images_db/"


def getDataPath(movieName):
    return DATABASE_DIR + movieName + '/' + 'data.json'

def save_2_jason(classification, kps, des, path):
    data = {}  
    cnt = 0
    data['classification'] = classification
    data['descriptors'] = np.asarray(des).tolist()
    data
    for i in kps:
        data['KeyPoint_%d'%cnt] = []  
        data['KeyPoint_%d'%cnt].append({'x': i.pt[0]})
        data['KeyPoint_%d'%cnt].append({'y': i.pt[1]})
        data['KeyPoint_%d'%cnt].append({'size': i.size})
        cnt+=1
    with open(path, 'w') as outfile:  
        json.dump(data, outfile)


def read_from_jason(path):
    des = []
    kps = []   
    classification = 0
    with open(path) as json_file:  
        data = json.load(json_file)
        classification = data['classification']
        des = np.array(data['descriptors'], dtype=np.float32)
        cnt = 0
        while(data.__contains__('KeyPoint_%d'%cnt)):
            pt = cv2.KeyPoint(x=data['KeyPoint_%d'%cnt][0]['x'],y=data['KeyPoint_%d'%cnt][1]['y'], _size=data['KeyPoint_%d'%cnt][2]['size'])
            kps.append(pt)
            cnt+=1
    return classification, kps, des

def createPoster(movieName, classification, imagePath):
    dir = DATABASE_DIR + movieName

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
    sift = cv2.SIFT.create()
    kp, des = sift.detectAndCompute(image2, None)


    #Save descriptors and keypoints in file
    save_2_jason(classification, kp, des, getDataPath(movieName))


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
