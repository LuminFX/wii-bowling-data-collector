import pytesseract
import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

ret, img = cap.read()

refined_frame = img

norm_frame = np.zeros((refined_frame.shape[0], refined_frame.shape[1]))
refined_frame = cv.normalize(refined_frame, norm_frame, 0, 255, cv.NORM_MINMAX)

# DENOISE
refined_frame = cv.fastNlMeansDenoisingColored(refined_frame, None, 10, 10, 7, 15)

# Grayscale image
refined_frame = cv.cvtColor(refined_frame, cv.COLOR_BGR2GRAY)

# threshold image
refined_frame = cv.threshold(refined_frame, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]

x = 1120
y = 420
w = 240
h = 80

refined_frame = refined_frame[y:y+h, x:x+w]

width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

# Print the resolution
print("Resolution: {}x{}".format(width, height))

cv.imshow("refined", refined_frame)

print(pytesseract.image_to_string(refined_frame, config='--psm 11 --oem 3 outputbase digits'))

cv.waitKey(0)