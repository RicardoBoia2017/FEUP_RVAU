import sys
import os
import cv2

movieName = sys.argv[1]
classification = sys.argv[2]
imagePath = sys.argv[3]

rootdir = "images_db"

image = cv2.imread(imagePath)
fullName = rootdir + '/' + movieName + '_' + classification + '.' + imagePath.split('.')[1] 
cv2.imshow('Feature points', image)
cv2.waitKey(0)

if os.path.isfile(fullName) is False:
    print("entrou")
    cv2.imwrite(fullName, image)