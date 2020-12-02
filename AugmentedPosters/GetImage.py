import os
import re
import cv2
import sys
import numpy as np

movieName = sys.argv[1]
rootdir = "images_db"
regex = re.compile(movieName + '_\d.(gif|jpe?g|tiff?|png|webp|bmp)')

image = None

for root, dirs, files in os.walk(rootdir):
  for name in files:
    if regex.match(name):
        fullName = name
        score = name.split('_')[1][0:1]
        image = cv2.imread(rootdir + '/' + name)

if image is None:
    sys.exit()

print("Score: " + score)

featurePoints = image.copy()
gray = cv2.cvtColor(featurePoints,cv2.COLOR_BGR2GRAY)

corners = cv2.goodFeaturesToTrack(gray, 500, 0.01, 1)
                              
corners = np.int0(corners)

for i in corners:
    x, y = i.ravel()
    cv2.circle(featurePoints, (x,y), 3, (255, 0, 255), -1)

if os.path.isfile(rootdir + '/feature_' + fullName) is False:
    cv2.imwrite(rootdir + '/feature_' + fullName, featurePoints)

cv2.imshow('Image', image)
cv2.imshow('Feature points', featurePoints)
cv2.waitKey(0)
