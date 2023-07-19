# wii-bowling-data-collector

The Wii Bowling Data Collector (WBDC) is built to record game information from Wii bowling through the use of a capture card. 

WBDC was built for the data-collection step of a longer-term project to reverse engineer the Wii Bowling MMR system.

## Description

WBDC records starting MMR, game score, and resultant MMR change from games of Wii Sports Bowling. To do this, a capture card video feed is taken from the Wii and processed with openCV and pytesseract. This information is tracked accross multiple games and is saved to a .csv file upon termination.

## Getting Started

### Dependencies

* Windows 10 (untested on MacOS / Linux)
* Python 3.11.4
* Pip 23.2

### Installing

* To install requirements, run
  ```
  Make install
  ```

### Executing

* To run program:
   ```
   Make run
   ```

### Known Issues

* Pytesseract struggles to read some of the text on screen due to the low resolution output of the Wii. Due to this, it 'sticks' for a while in the MMR reading loop. Given time, the program continues, however this time is quite inconsistent.
* WBDC Will occasionally have difficulty reading the bowling score when a new Wii record is set.
