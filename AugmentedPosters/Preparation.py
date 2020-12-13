import sys
import os
import cv2
import numpy as np

movieName = sys.argv[1]
classification = sys.argv[2]
imagePath = sys.argv[3]

dir = "images_db/" + movieName

#Check if poster already exists in databases
if os.path.isdir(dir) is True:
    print("Directory already exists")
    sys.exit()

#Create directory
os.mkdir(dir)

#Create Image
image = cv2.imread(imagePath)
cv2.imwrite(dir + '/' + movieName + '_' + classification + '.' + imagePath.split('.')[1] , image)

#Create features files
image2 = cv2.imread(dir + '/' + movieName + '_' + classification + '.' + imagePath.split('.')[1])
sift = cv2.xfeatures2d_SIFT.create()
kp, des = sift.detectAndCompute(image2, None)

#Save descriptors and keypoints in file
np.save(dir + "/descriptors", des)

