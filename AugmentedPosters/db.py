import numpy as np
import json
import cv2
import os

DATABASE_DIR = "images_db"

class Poster:
    def __init__(self, imagePath, movieName, score, kp, descriptors):
        self.movieName = movieName
        self.score = score
        self.kp = kp
        self.descriptors = descriptors
        self.image = cv2.imread(imagePath)
        
def getDataPath(movieName):
    return DATABASE_DIR + "/" + movieName + '/' + 'data.json'

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

#Get posters from database
def retrieveImages():
    targets = []

    for _, dirs, _ in os.walk(DATABASE_DIR):
        for subdir in dirs:
            for _, _, files2 in os.walk(DATABASE_DIR + "/" + subdir):
                descriptors = []
                kp = []
                score = 0
                for name in files2:
                    if name == "data.json":
                        score, kp, descriptors = readjson(getDataPath(subdir))
                    else:
                        imagePath = DATABASE_DIR + '/' + subdir + '/' + name
                        
            targets.append(Poster(imagePath, subdir, score, kp, descriptors))
    
    return targets