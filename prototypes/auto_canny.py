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
for imagePath in glob.glob(args["images"] + "/*square.png"):
	# load the image, convert it to grayscale, and blur it slightly
	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (3, 3), 0)

	# apply Canny edge detection using a wide threshold, tight
	# threshold, and automatically determined threshold
	wide = cv2.Canny(blurred, 10, 200)
	tight = cv2.Canny(blurred, 225, 250)
	auto = auto_canny(blurred)

	i = np.argwhere(wide == 255)
	t = tuple(map(tuple, i))
	t_sort = sorted(t, key=lambda p: atan2(p[1], p[0]))
	# filter list causing werid interpolate
	# TODO

	line = LineString(t_sort)
	n = 80 # num points
	distances = np.linspace(0, line.length, n)
	points = [line.interpolate(distance) for distance in distances]
	new_line = LineString(points)

	x,y = new_line.xy
	print(len(i[:,0]))
	plt.scatter(i[:,0], i[:,1])
	plt.scatter(x, y)
	plt.show()

	# show the images
	resize1 = ResizeWithAspectRatio(image, height=360)
	# cv2.imshow("Original", resize1)
	resize2 = ResizeWithAspectRatio(np.hstack([wide, tight, auto]), height=360)
	# cv2.imshow("Edges", resize2)
	cv2.waitKey(0)
