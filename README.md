## Framefinder

This script handles the following use case. You have a picture (like screen capture) from movie, but you don't know where 
this picture happens in the movie timeline.

Supposedly you stumbled upon youtube mashup from the movie that you have on disk, now you want
to find this exact moment in the movie when given shot happens.

It uses computer vision library (cv2) to search video frame by frame and match the picture with each frame fuzzily.
