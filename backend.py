import cv2
import pytesseract
from PIL import Image
import numpy as np
import os

# Path to Tesseract OCR (Update this path if needed)
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'  # Adjust for your OS

# Read image using PIL
file_path = "image/ibupro.png"
img = Image.open(file_path)

# Convert PIL Image to OpenCV format
img_cv = np.array(img)

# Convert RGB to BGR for OpenCV compatibility
img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)

# Convert to grayscale using OpenCV
gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

# Apply OTSU thresholding
ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

# Specify structure shape and kernel size for dilation
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

# Apply dilation
dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

# Find contours
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# Make a copy of the image to draw rectangles
im2 = img_cv.copy()

# Create an empty file for recognized text
with open("recognized.txt", "w") as file:
    file.write("")

# Loop through contours and extract text
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    
    # Draw a rectangle around the detected text
    rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Crop the text block
    cropped = im2[y:y + h, x:x + w]
    
    # Apply OCR on the cropped image
    text = pytesseract.image_to_string(cropped)
    
    # Append extracted text to file
    with open("recognized.txt", "a") as file:
        file.write(text + "\n")

print("Text extraction complete. Check recognized.txt for output.")
