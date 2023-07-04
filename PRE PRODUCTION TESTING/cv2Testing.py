import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import pytesseract
import time
from PIL import Image

# img = cv.imread("bowlingFrame.jpg")

# if img is not None:
#     cv.imshow("Display Window", img)
#     k = cv.waitKey(0)

cap = cv.VideoCapture(0)

scoreTemplate = cv.imread("scoreRef.png")

if (not cap.isOpened()) or (scoreTemplate is None):
    print("cam not open")
    exit()

while True:

    time.sleep(0.5)

    #capture frame by frame
    ret, frame = cap.read()

    if not ret:
        print("Cant get frame... exiting")
        break

    lower = np.array([120, 40, 0])
    upper = np.array([250, 170, 120])

    mask = cv.inRange(frame, lower, upper)
    output = cv.bitwise_and(frame, frame, mask=mask)

    ret, thresh = cv.threshold(mask, 40, 255, 0)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    if len(contours) != 0:

        cv.drawContours(output, contours, -1, 255, 3)
        c = max(contours, key = cv.contourArea)
        x,y,w,h = cv.boundingRect(c) # create x, y, width, and height bounds

        if (abs(w-h) <= 70) and w > 150:

            cropped_frame = frame[y:y+h, x:x+w]

            # cv.rectangle(output,(x,y),(x+w,y+h),(0,255,0),2) # adds rectangle to output view
            # cv.imshow("Result", np.hstack([frame, output]))

            cv.imshow("Cropped frame", cropped_frame)
        
            cropped_frame_mask = mask[y:y+h, x:x+w]
            refined_frame = cropped_frame.copy()

            #refine the image

            # STEP 1: NORMALIZE

            norm_frame = np.zeros((refined_frame.shape[0], refined_frame.shape[1]))
            refined_frame = cv.normalize(refined_frame, norm_frame, 0, 255, cv.NORM_MINMAX)

            # DENOISE

            refined_frame = cv.fastNlMeansDenoisingColored(refined_frame, None, 10, 10, 7, 15)

            # Grayscale image

            refined_frame = cv.cvtColor(refined_frame, cv.COLOR_BGR2GRAY)

            # threshold image

            refined_frame = cv.threshold(refined_frame, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]

            print(pytesseract.image_to_string(refined_frame, config='--psm 11 --oem 3 outputbase digits'))

            cv.imshow("Refined frame", refined_frame)
        
        else:
            cv.imshow("frame", frame)
    
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()