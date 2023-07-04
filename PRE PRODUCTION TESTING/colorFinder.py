import cv2 as cv
import numpy as np
import pytesseract

img = cv.imread("baseScoreRef.png")

lower = np.array([140, 40, 0])
upper = np.array([250, 150, 50])

mask = cv.inRange(img, lower, upper)
output = cv.bitwise_and(img, img, mask=mask)

ret, thresh = cv.threshold(mask, 40, 255, 0)
contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

if len(contours) != 0:
    cv.drawContours(output, contours, -1, 255, 3)
    c = max(contours, key = cv.contourArea)
    x,y,w,h = cv.boundingRect(c)
    cv.rectangle(output,(x,y),(x+w,y+h),(0,255,0),2)

cv.imshow("Result", np.hstack([img, output]))

cv.waitKey(0)