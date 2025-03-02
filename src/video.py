
# Importing OpenCV
import cv2
import pytesseract
import numpy as np
import platform 
import os
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


def video_detect():
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

        if ((count % 30) == 0):
            height, width, _ = frame.shape

            x_coor, y_coor, full_width, full_height = 0,0, width, height

            recognized_text = pytesseract.image_to_string(frame).strip()
            bounding_box_info = pytesseract.image_to_boxes(frame)

            for b in bounding_box_info.splitlines():
                b = b.split(' ')
                x, y, xtop_right, ytop_right = int(b[1]), int(b[2]), int(b[3]), int(b[4])
                cv2.rectangle(frame, (x, height-y),
                        (xtop_right, height - ytop_right), (128,0,128), 4)

            if recognized_text:
                with open("video_detected_text.txt", "w") as text_file:
                    text_file.write(recognized_text + "\n")

            cv2.imshow('Pill Bottle Detection',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    video.release()
    cv2.destroyAllWindows()


def parseText(text_file, json_file):
    # Load JSON data
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Extract drug data and use lowercase for comparison
    drug_info = {drug["medicinal_name"].lower(): drug for drug in data["drugs"]}

    # Read extracted text file
    with open(text_file, "r") as file:
        text_content = file.read().lower()  # Convert entire text to lowercase

    # Use a set to track found drug names
    found_drugs = set()
    results = []

    # Check if any medicinal name is present in the text
    for drug_name in drug_info:
        if drug_name in text_content and drug_name not in found_drugs:
            results.append(drug_info[drug_name])
            found_drugs.add(drug_name)  # Ensure it doesn't get added again

    return results


if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = detectTesseract()
    
    video_detect()

    parsed_results = parseText("video_detected_text.txt", "data/drug.json")
    if parsed_results:
        print("-" * 50)
        for result in parsed_results:
            print(f"Medicinal Name: {result['medicinal_name']}")
            print(f"Generic Name: {result['generic_name']}")
            print(f"Purpose: {result['purpose']}")
            print(f"Usage: {result['usage']}")
            print(f"Warning: {result['warning']}")
        print("-" * 50)
    else:
        print("No matches found.")