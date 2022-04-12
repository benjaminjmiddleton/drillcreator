import glob
import math

import cv2
import numpy as np
from shapely.geometry import LineString


def auto_canny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)

	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)

	# return the edged image
	return edged

def interpret_image(filepath, num_points, centered=True, relative_path=False):
	if relative_path:
		imagePath = glob.glob(f"./{filepath}")[0]
	else:
		imagePath = glob.glob(filepath)[0]
	# Init
	total = 0
	ntotal = 0
	run = 1
	points_pos = []

	# load the image, convert it to grayscale, and blur it slightly
	image = cv2.imread(imagePath)
	dimension = image.shape
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (3, 3), 0)

	# apply Canny edge detection using a automatically determined threshold
	auto = auto_canny(blurred)

	# Don't really get this but is matters
	threshold = cv2.threshold(auto,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]

	contours, heirarchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	# Get total number of points in contours
	for contour in contours:
		total += contour.size

	for contour in contours:
		# reshape array to include tuples
		t = np.reshape(contour, (-1,2))  
		n = int(num_points*(contour.size/total)) # num points to add for countour
		if t.size > 2 and n > 1:
			line = LineString(t)
			ntotal += n
			# make last contour have any extra points
			if run == len(contours):
				n += (num_points - ntotal)
			distances = np.linspace(0, line.length, n)
			# Points along coontour
			points = [line.interpolate(distance) for distance in distances]
			new_line = LineString(points)
			x, y = new_line.xy
			if centered:
				x=np.subtract(x, (math.ceil(dimension[1]/2)))
				y=np.subtract(y, (math.ceil(dimension[0]/2)))
			points_pos += list(zip(x, y))
		run += 1
	return points_pos

def vis_points(filepath, x, y):
	imagePath = glob.glob(f"./{filepath}")[0]
	image = cv2.imread(imagePath)
	h, w = image.shape[:2]
	vis = np.zeros((h, w, 3), np.uint8)
	vis[np.asarray(y, int), np.asarray(x, int)] = (255,255,255)
	vis = np.concatenate((image, vis), axis=1)
	cv2.imshow(imagePath, vis)
	cv2.waitKey(0)

if __name__ == "__main__":
	points = interpret_image("test_images/square.png", 260, relative_path=True)
	x, y = map(list,zip(*points))
	vis_points("test_images/bearcat.png", x, y)
		