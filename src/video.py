# Importing OpenCV
import cv2
import pytesseract
import numpy as np
import os
import platform
import json

def detectTesseract():
    system_os = platform.system()
    tesseract_path = None

    # macOS
    if system_os == "Darwin":
        # M1/M2 Mac
        tesseract_path = "/opt/homebrew/bin/tesseract"

        # Intel Mac
        if not os.path.exists(tesseract_path):
            tesseract_path = "/usr/local/bin/tesseract"
    elif system_os == "Windows":
        tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    else:
        raise Exception("Unsupported OS")

    return tesseract_path

pytesseract.pytesseract.tesseract_cmd = detectTesseract()

# Reading the video from the webcam
video = cv2.VideoCapture(0)

font_scale = 2.0
font = cv2.FONT_HERSHEY_DUPLEX

# Checking whether the camera has been accessed using the isOpened function
if (video.isOpened() == False):
    print("Unable to Open Video")

count = 0
while True:
    ret, frame = video.read()
    count += 1

    if ((count % 5) == 0):
        height, width, _ = frame.shape

        x_coor, y_coor, full_width, full_height = 0,0, width, height

        recognized_text = pytesseract.image_to_string(frame).strip()
        bounding_box_info = pytesseract.image_to_boxes(frame)

        for b in bounding_box_info.splitlines():
            b = b.split(' ')
            x, y, xtop_right, ytop_right = int(b[1]), int(b[2]), int(b[3]), int(b[4])
            cv2.rectangle(frame, (x, height-y),(xtop_right, height - ytop_right), (128,0,128), 4)

        if recognized_text:
            with open("video_detected_text.txt", "w") as text_file:
                text_file.write(recognized_text + "\n")
        cv2.imshow('Pill Bottle Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

video.release()
cv2.destroyAllWindows()
