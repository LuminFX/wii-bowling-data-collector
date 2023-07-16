import os
import driverHelpers as dh
import cv2 as cv
from scoreScraper import scoreScraper
import time

os.system('cls')

nameASCII = """
 __      __.__.__  __________              .__  .__                 ________          __           _________        .__  .__                 __                
/  \    /  \__|__| \______   \ ______  _  _|  | |__| ____    ____   \______ \ _____ _/  |______    \_   ___ \  ____ |  | |  |   ____   _____/  |_  ___________ 
\   \/\/   /  |  |  |    |  _//  _ \ \/ \/ /  | |  |/    \  / ___\   |    |  \|__  \|   __\__  \   /    \  \/ /  _ \|  | |  | _/ __ \_/ ___\   __\/  _ \_  __ \ 
 \        /|  |  |  |    |   (  <_> )     /|  |_|  |   |  \/ /_/  >  |    `   \/ __ \|  |  / __ \_ \     \___(  <_> )  |_|  |_\  ___/\  \___|  | (  <_> )  | \/
  \__/\  / |__|__|  |______  /\____/ \/\_/ |____/__|___|  /\___  /  /_______  (____  /__| (____  /  \______  /\____/|____/____/\___  >\___  >__|  \____/|__|   
       \/                  \/                           \//_____/           \/     \/          \/          \/                      \/     \/                   """
print(nameASCII)

ss = scoreScraper()
user_input = None

while True: # set number of players to track
    user_input = input("Enter the number of players to track (currently support 1 player max): ")
    if dh.validIntInput(user_input, 1, 1): #ensures only one player is allowed to play
        ss.num_players = int(user_input)
        break
    print("Invalid player count! Try again.")

for i in range(int(user_input)): # set starting player MMRs
    while True:
        user_input = input("Would you like to load a save file for player " + str(i+1) + "? (y/n): ")
        if user_input == 'y':
            success = False
            while not success:
                user_input = input("Please input save file name (or q to go back): ")
                if user_input == 'q':
                    break;
                success = ss.readScoreData(user_input, i)
                if not success:
                    print("There was an error finding or loading this file. Please try again.")
            if success: 
                print("MMR of " + str(ss.score_data[i][-1][1] + ss.score_data[i][-1][2]) + " loaded successfully!")
                break;
        else:
            while True:
                user_input = input("Please input MMR for player " + str(i+1) + ": ")
                if dh.validIntInput(user_input, 0, 2000):
                    ss.starting_MMRs.append(int(user_input))
                    break
                print("Invalid MMR! Try again.")
            break;

while True: # set capture device
    user_input = input("Enter the capture card device number (likely 1 if you have a webcam and 0 if you don't): ")
    if dh.validIntInput(user_input, 0, 10):
        print("A preview window has opened. Examine and press any key to close.")
        ret = ss.setCaptureDevice(int(user_input))
        if ret:
            ss.printCaptureFrame()
            user_input = input("Did that look correct? (y/n): ")
            if user_input == 'y':
                break
        else: print("An image could not be loaded from this device.")
    else: print("That is not a valid input. Try again.")

print("You may start to play! Keep this window open. Information will be printed as you go!")

while True:

    time.sleep(0.5)

    while True: # loop until a correct score is found and validated

        ret = ss.scanForScore()
        if ret:
            print("Score captured!")
            for i in range(ss.num_players):
                print("Player " + str(i+1) + ": " + str(ss.score_data[i][ss.games_stored][0]))
            user_input = input("Is this correct? (y/n)")
            if user_input == 'y':
                break
            else:
                for i in range(ss.num_players):
                    del ss.score_data[i][ss.games_stored]

    while True: #loop until a correct mmr change is found and validated
        ret = ss.scanForMMRChange()
        if ret:
            print("MMR Change Captured!")
            for i in range(ss.num_players):
                print("Player " + str(i+1) + ": " + str(ss.score_data[i][ss.games_stored-1][2]))
            user_input = input("Is this correct? (y/n)")
            if user_input == 'y':
                break
            else:
                ss.games_stored -= 1
                for i in range(ss.num_players):
                    temp_list = [ss.score_data[i][ss.games_stored][0]]
                    del ss.score_data[i][ss.games_stored]
                    ss.score_data[i].append(temp_list)

    user_input = input("Would you like to play another game? (y/n)")
    if user_input == 'n':
        break

print("Saving data...")

for i in range(int(ss.num_players)):
    user_input = input("Please enter the name for player " + str(i+1) + "'s save file: ")
    ss.writeScoreData(user_input, i)
    print("Data for " + user_input + " has been saved.")