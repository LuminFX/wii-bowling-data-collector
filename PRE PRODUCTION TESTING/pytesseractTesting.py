from PIL import Image
import pytesseract

print(pytesseract.image_to_string(Image.open('bowlingFrame.jpg'), config='--psm 11 --oem 1 outputbase digits'))

