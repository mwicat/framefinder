import datetime
import sys

import cv2
import numpy as np
import progressbar


vid_fn = sys.argv[1]
img_fn = sys.argv[2]

methods = (
	("Correlation", cv2.HISTCMP_CORREL),
	("Chi-Squared", cv2.HISTCMP_CHISQR),
	("Intersection", cv2.HISTCMP_INTERSECT), 
	("Hellinger", cv2.HISTCMP_BHATTACHARYYA))

vidcap = cv2.VideoCapture(vid_fn)

my_img = cv2.imread(img_fn)

# extract a 3D RGB color histogram from the image,
# using 8 bins per channel, normalize, and update
# the index
def get_hist(img):
	hist = cv2.calcHist([img], [0, 1, 2], None, [8, 8, 8],
			[0, 256, 0, 256, 0, 256])
	hist = hist.flatten()
	return hist

my_img_hist = get_hist(my_img)

success = True
count = 0

num_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = vidcap.get(cv2.CAP_PROP_FPS)

results = {
	method_name: np.zeros(num_frames)
	for method_name, method_id in methods
}

with progressbar.ProgressBar(max_value=num_frames) as bar:
	for pos in xrange(num_frames):
	  success, vid_img = vidcap.read()
	  if not success:
	  	break
	  vid_hist = get_hist(vid_img)
	  for method_name, method_id in methods:
		  d = cv2.compareHist(my_img_hist, vid_hist, method_id)
		  results[method_name][pos] = d
	  bar.update(pos)


def get_far(arr, count, how_far):
	r = []
	for x in arr:
		is_far = all(abs(x-xr) >= how_far for xr in r)
		if is_far and x not in r:
			r.append(x)
		if len(r) == count:
			break
	return r


for method_name, results in results.iteritems():
	print method_name
	guesses = results.argsort()[::-1]
	time_far = 5 * fps
	guesses = get_far(guesses, 3, time_far)
	for frame in guesses:
		time_s = frame / fps
		timecode = str(datetime.timedelta(seconds=time_s))
		print timecode
		vidcap.set(1, frame)
		success, image = vidcap.read()
		cv2.imwrite("frame_%s.jpg" % timecode, image)

