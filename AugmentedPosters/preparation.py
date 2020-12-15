import sys
import os
import cv2
import numpy as np
import camera_calibration as cam
import util
import argparse
import json

DATABASE_DIR = "images_db/"


def getDataPath(movieName):
    return DATABASE_DIR + movieName + '/' + 'data.json'

def save2json(score, kps, des, path):
    data = {}  
    cnt = 0
    data['score'] = score
    data['descriptors'] = np.asarray(des).tolist()
    for i in kps:
        data['KeyPoint_%d'%cnt] = []  
        data['KeyPoint_%d'%cnt].append({'x': i.pt[0]})
        data['KeyPoint_%d'%cnt].append({'y': i.pt[1]})
        data['KeyPoint_%d'%cnt].append({'size': i.size})
        cnt+=1
    with open(path, 'w') as outfile:  
        json.dump(data, outfile)


def readjson(path):
    des = []
    kps = []   
    score = 0
    with open(path) as json_file:  
        data = json.load(json_file)
        score = int(data['score'])
        des = np.array(data['descriptors'], dtype=np.float32)
        cnt = 0
        while(data.__contains__('KeyPoint_%d'%cnt)):
            pt = cv2.KeyPoint(x=data['KeyPoint_%d'%cnt][0]['x'],y=data['KeyPoint_%d'%cnt][1]['y'], _size=data['KeyPoint_%d'%cnt][2]['size'])
            kps.append(pt)
            cnt+=1
    return score, kps, des



def createPoster(movieName, score, imagePath):
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
    sift = util.sift_create()

    gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)   
    kp, des = sift.detectAndCompute(gray, None)

    #Save descriptors keypoints and score in file
    save2json(score, kp, des, getDataPath(movieName))



def main():

    parser = argparse.ArgumentParser(description='Prepare setup')
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('--add', '-a', nargs=3, metavar=('name', 'score', 'path'), action='store')
    group.add_argument('--calibrate', '-c', action='store_true')
    group.add_argument('--clean', action='store_true')

    args = parser.parse_args()

    if args.calibrate:
        cam.calibrate()
    
    if args.add:
        name = args.add[0]
        score = args.add[1]
        path = args.add[2]
        createPoster(name, score, path)

    if args.clean:
        cam.delete()


if __name__ == "__main__":
    main()
