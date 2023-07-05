import os
import driverHelpers as dh
import cv2 as cv
from scoreScraper import scoreScraper
import time

os.system('cls')

nameASCII = """
 __      __.__.__  __________              .__  .__                 ________          __             _________                                        
/  \    /  \__|__| \______   \ ______  _  _|  | |__| ____    ____   \______ \ _____ _/  |______     /   _____/ ________________  ______   ___________ 
\   \/\/   /  |  |  |    |  _//  _ \ \/ \/ /  | |  |/    \  / ___\   |    |  \|__  \|   __\__  \    \_____  \_/ ___\_  __ \__  \ \____ \_/ __ \_  __ \ 
 \        /|  |  |  |    |   (  <_> )     /|  |_|  |   |  \/ /_/  >  |    `   \/ __ \|  |  / __ \_  /        \  \___|  | \// __ \|  |_> >  ___/|  | \/
  \__/\  / |__|__|  |______  /\____/ \/\_/ |____/__|___|  /\___  /  /_______  (____  /__| (____  / /_______  /\___  >__|  (____  /   __/ \___  >__|   
       \/                  \/                           \//_____/           \/     \/          \/          \/     \/           \/|__|        \/       """
print(nameASCII)

ss = scoreScraper()
user_input = None

while True: # set number of players to track
    user_input = input("Enter the number of players to track: ")
    if dh.validIntInput(user_input, 1, 4):
        ss.num_players = int(user_input)
        break
    print("Invalid player count! Try again.")

for i in range(int(user_input)): # set starting player MMRs
    while True:
        user_input = input("Please input MMR for player " + str(i+1) + ": ")
        if dh.validIntInput(user_input, 0, 2000):
            ss.starting_MMRs.append(int(user_input))
            break
        print("Invalid MMR! Try again.")

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

    while True:

        ret = ss.scanForScore()
        if ret:
            print("Score captured!")
            print(ss.score_data)
            for i in range(ss.num_players):
                print("Player " + str(i+1) + ": " + str(ss.score_data[i][ss.games_stored][0]))
            print(ss.score_data)
            user_input = input("Is this correct? (y/n)")
            if user_input == 'y':
                break
            else:
                for i in range(ss.num_players):
                    del ss.score_data[i][ss.games_stored]

    while True:
        ret = ss.scanForMMRChange()
        if ret:
            print("MMR Captured!")
            for i in range(ss.num_players):
                print("Player " + str(i+1) + ": " + str(ss.score_data[i][ss.games_stored-1][2]))
            print(ss.score_data)
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

        


