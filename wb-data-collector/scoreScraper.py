'''
Main tracking class from wii-bowling-data-collector

A scoreScraper object manages player bowling scores, MMRs, the capture device,
and contains all functions needed to extract data from a capture card feed of 
Wii Sports Bowling.
'''

import cv2 as cv
import numpy as np
import pytesseract
import csv
import os.path
import ast

class scoreScraper:
    starting_MMRs = []
    games_stored = 0
    num_players = 0

    score_bounds = []
    found_score_bounds = False

    capture_device = None
    score_data = [[],[],[],[]] # will hold data in the form of [Game Score, Starting MMR, MMR Change]

    def __init__(self):
        return
    
    def __del__(self):
        self.capture_device.release()

    """
    readScoreData

    Reads score data from a .csv file, formats it into a list within a list, and sets
    games_stored, score_data, and starting_MMRs to correct values

    Takes in a file_name with .csv included in the name and a player index between 0 and 3 (inclusive)

    Returns bool based on success

    """

    def readScoreData(self, file_name, player_index): # will read existing score database from profided file

        if os.path.isfile(file_name):
            with open(file_name, newline="") as file:
                reader = csv.reader(file)
                data = list(reader)

            if len(data) == 0: return False

            converted_data = []

            for row in data:
                converted_row = ast.literal_eval(row[0])
                converted_data.append(converted_row)
                self.games_stored+=1

            self.score_data[player_index] = converted_data
            self.starting_MMRs.append(converted_data[-1][1] + converted_data[-1][2])

            return True

        return False
    

    """
    writeScoreData

    Writes a player's score data (mmr and gamescores) to a CSV file.

    Takes in a file name with no ".csv" extension and a player index between 0 and 3 (inclusive)
    """
    def writeScoreData(self, file_name, player_index): # will write data to file upon close

        if os.path.exists(file_name+".csv"):
            os.remove(file_name+".csv") 

        with open(file_name+".csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows([[item] for item in self.score_data[player_index]])

    """
    scanForScore

    scanForScore captures a frame from the selected capture device and scans for a bowling score.
    
    Returns boolean value based on success

    """

    def scanForScore(self): # will take a frame from capture device and try to scrub for score

        ret, frame = self.capture_device.read()
        ret = self.setScoreBounds(frame)

        if not ret: return False

        for i in range(self.num_players):

            score_list = []
            count = 0
            
            while count < 5:
                
                count += 1

                ret, frame = self.capture_device.read()

                x = self.score_bounds[i][0]
                y = self.score_bounds[i][1]
                w = self.score_bounds[i][2]
                h = self.score_bounds[i][3]

                cropped_frame = frame[y:y+h, x:x+w]
                refined_frame = self.imgproc(cropped_frame, True)

                curr_read = pytesseract.image_to_string(refined_frame, config='--psm 11 --oem 3 outputbase digits')
                ret, processed_score = self.processString(curr_read, 0 ,300)

                if ret:
                    score_list.append(processed_score)

            if not len(score_list) == 0:
                self.score_data[i].append([self.pickFrequentNumber(score_list)])
            else:
                return False
        return True
    
    """
    scanForMMRChange

    scanForMMRChange captures a frame from the selected capture device and scans for a mmr score and calculates the change.
    
    Returns boolean value based on success

    """

    def scanForMMRChange(self): # will take a frame from capture device and try to find the mmr change
        
        print("Scanning for mmr")

        ret, frame = self.capture_device.read()

        x = 1120
        y = 420
        w = 240
        h = 80
    
        for i in range(self.num_players):

            mmr_list = []
            count = 0
            
            while count < 6:

                ret, frame = self.capture_device.read()

                cropped_frame = frame[y:y+h, x:x+w]
                refined_frame = self.imgproc(cropped_frame, False)

                curr_read = pytesseract.image_to_string(refined_frame, config='--psm 11 --oem 3 outputbase digits')
                ret, processed_score = self.processString(curr_read, 0, 2000)

                if ret:
                    count += 1
                    mmr_list.append(processed_score)

            if not len(mmr_list) == 0:

                if self.games_stored == 0:
                    self.score_data[i][self.games_stored].append(self.starting_MMRs[i])
                    self.score_data[i][self.games_stored].append(self.pickFrequentNumber(mmr_list) - self.starting_MMRs[i]) 
                else:
                    self.score_data[i][self.games_stored].append(self.score_data[i][self.games_stored-1][1] + self.score_data[i][self.games_stored-1][2])
                    self.score_data[i][self.games_stored].append(self.pickFrequentNumber(mmr_list) - (self.score_data[i][self.games_stored][1]))
            else:
                return False
        
        self.games_stored += 1
        return True

    """
    setCaptureDevice

    Takes in device number and sets cap device for later use
    """

    def setCaptureDevice(self, device_number): # Sets the capture device number for reference elsewhere
        cap = cv.VideoCapture(device_number)
        if (cap.isOpened()):
            self.capture_device = cap
            return True
        return False
    
    """
    processString

    cleans an input string and returns a number between bounds with no other characters

    takes in an input, low bound, and high bound
    """

    def processString(self, input, low, high): # take input and return if the clean data is represented as a bowling score
        numbers_only = ''.join(c for c in input if c.isdigit())
        if numbers_only:
            numbers_int = int(numbers_only)
            if (numbers_int >= low) and (numbers_int <= high):
                return True, numbers_int
        return False, -1
    
    """
    getScoreBound

    finds crop area for score reading from an input frame using openCV
    """

    def setScoreBounds(self, frame):
        retVal = False
        for i in range(self.num_players):
            match i:
                case 0:
                    lower = np.array([120, 40, 0]) # bounds for blue 
                    upper = np.array([250, 170, 120])
                case 1:
                    lower = np.array([120, 40, 0]) # bounds for red
                    upper = np.array([250, 170, 120])
                case 2:
                    lower = np.array([120, 40, 0]) # bounds for green 
                    upper = np.array([250, 170, 120])
                case 3:
                    lower = np.array([120, 40, 0]) # bounds for gold
                    upper = np.array([250, 170, 120])
        
            mask = cv.inRange(frame, lower, upper)
            output = cv.bitwise_and(frame, frame, mask=mask)

            ret, thresh = cv.threshold(mask, 40, 255, 0)
            contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

            if len(contours) != 0:
                c = max(contours, key = cv.contourArea)
                x,y,w,h = cv.boundingRect(c) # create x, y, width, and height bounds

                if (abs(w-h) <= 70 and abs(w-h) >= 20) and w > 310:
                    self.score_bounds.append([x,y,w,h])
                    self.found_score_bounds = True
                    retVal = True

        return retVal
    
    """
    pickFrequentNumber

    returns most frequent number in list
    """

    def pickFrequentNumber(self, list):
        return max(set(list), key=list.count)
    
    """
    improc

    processes passed in frame to prepare it for pytesseract text recognition
    """

    def imgproc(self, frame, inverted):
        
        refined_frame = frame.copy()

        norm_frame = np.zeros((refined_frame.shape[0], refined_frame.shape[1]))
        refined_frame = cv.normalize(refined_frame, norm_frame, 0, 255, cv.NORM_MINMAX)
        # DENOISE
        refined_frame = cv.fastNlMeansDenoisingColored(refined_frame, None, 10, 10, 7, 15)
        # Grayscale image
        refined_frame = cv.cvtColor(refined_frame, cv.COLOR_BGR2GRAY)
        # threshold image

        if inverted: refined_frame = cv.threshold(refined_frame, 148, 255, cv.THRESH_BINARY_INV)[1]
        else: refined_frame = cv.threshold(refined_frame, 148, 255, cv.THRESH_BINARY)[1]

        return refined_frame