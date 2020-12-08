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
image2 = cv2.imread(dir + '/' + movieName + '_' + classification + '.' + imagePath.split('.')[1])

#Create features files
orb = cv2.ORB_create(nfeatures = 1000)
kp, des = orb.detectAndCompute(image, None)
kp2, des2 = orb.detectAndCompute(image2, None)

#Save descriptors in file
np.save(dir + "/descriptors", des)

#Show image
#cv2.imshow('Image', image)
#cv2.waitKey(0)
