import argparse
import glob
from math import atan2

import cv2
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import LineString
from shapely.ops import unary_union


def auto_canny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)

	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)

	# return the edged image
	return edged

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,
	help="path to input dataset of images")
args = vars(ap.parse_args())

# loop over the images
for imagePath in glob.glob(args["images"] + "/*bearcat.png"):
	# load the image, convert it to grayscale, and blur it slightly
	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (3, 3), 0)

	# apply Canny edge detection using a automatically determined threshold
	auto = auto_canny(blurred)

	_, threshold = cv2.threshold(auto, 127, 255, cv2.THRESH_BINARY)
	contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	i = 0
	for contour in contours:
  
		# here we are ignoring first counter because 
		# findcontour function detects whole image as shape
		if i == 0:
			i = 1
			continue
	
		t = np.reshape(contour, (-1,2))  
	
		if t.size > 2:
			line = LineString(t)
			n = 80 # num points
			distances = np.linspace(0, line.length, n)
			points = [line.interpolate(distance) for distance in distances]
			new_line = LineString(points)
			x, y = new_line.xy
			plt.scatter(x, y)
	plt.gca().invert_yaxis()
	plt.show()
