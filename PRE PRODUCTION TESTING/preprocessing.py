import pytesseract
import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

ret, frame = cap.read()

lower = np.array([120, 40, 0]) # bounds for blue 
upper = np.array([250, 170, 120])

mask = cv.inRange(frame, lower, upper)
output = cv.bitwise_and(frame, frame, mask=mask)

ret, thresh = cv.threshold(mask, 40, 255, 0)
contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

if len(contours) != 0:
    c = max(contours, key = cv.contourArea)
    x,y,w,h = cv.boundingRect(c) # create x, y, width, and height bounds



while True:

    ret, img = cap.read()

    img = img[y:y+h, x:x+w]

    refined_frame = img

    norm_frame = np.zeros((refined_frame.shape[0], refined_frame.shape[1]))
    refined_frame = cv.normalize(refined_frame, norm_frame, 0, 255, cv.NORM_MINMAX)

    # DENOISE

    refined_frame = cv.fastNlMeansDenoisingColored(refined_frame, None, 10, 10, 7, 15)

    # Grayscale image

    refined_frame = cv.cvtColor(refined_frame, cv.COLOR_BGR2GRAY)

    # threshold image

    refined_frame = cv.threshold(refined_frame, 148, 255, cv.THRESH_BINARY_INV)[1]

    cv.imshow("refined", refined_frame)

    print(pytesseract.image_to_string(refined_frame, config='--psm 11 --oem 3 outputbase digits'))

    if cv.waitKey(1) == ord('q'):
            break
