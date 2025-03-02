import cv2
import pytesseract
# from PIL import Image
# import numpy as np
import os
import platform
import re       # for text cleaning the "TM, R" symbols


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

# removes trademark and registered symbols: ™, ®
def clean_text(text):
    text = re.sub(r"[™®]", "", text)        # remove trademark & registered symbols
    # text = re.sub(r"[ \t]+", " ", text)     # replace multiple spaces with a single space
    # return text.strip()                     # keeps new lines but remove leading/trailing spaces
    return text

def openImage(imageName):
    file_path = "image/" + imageName
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Image file '{file_path}' not found!")
    img = cv2.imread(file_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("Output", img)
    # cv2.waitKey(0)
    return img

def detectText(img):
    """Detects text using Tesseract and stores it in a file."""
    text = pytesseract.image_to_string(img)
    text = clean_text(text)
    
    # Save text to image_text.txt
    with open("image_text.txt", "w") as file:
        file.write(text)
    
    print("Extracted text saved to image_text.txt")
    return text

def draw_boxes_on_character(img):
    img_width = img.shape[1]
    img_height = img.shape[0]
    boxes = pytesseract.image_to_boxes(img)
    for box in boxes.splitlines():
        box = box.split(" ")
        character = box[0]
        x = int(box[1])
        y = int(box[2])
        x2 = int(box[3])
        y2 = int(box[4])

        # Draw GREEN bounding box
        cv2.rectangle(img, (x, img_height - y), (x2, img_height - y2), (0, 255, 0), 2)

        # Draw character label in GREEN
        cv2.putText(img, character, (x, img_height -y2), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)
    
    return img

def draw_boxes_on_text(img):
    # Return raw information about the detected texts
    raw_data = pytesseract.image_to_data(img)
    for count, data in enumerate(raw_data.splitlines()):
        if count > 0:
            data = data.split()
            if len(data) == 12:
                x, y, w, h, content = int(data[6]), int(data[7]), int(data[8]), int(data[9]), data[11]
                
                cv2.rectangle(img, (x, y), (w + x, h + y), (0, 255, 0), 2)
                cv2.putText(img, content, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
    return img


if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = detectTesseract()
    imageName = input("Enter Image Name with Extension (image.png): ")
    img = openImage(imageName)
    
    # detect text and store in file
    text = detectText(img)

    # draw bounding boxes on characters
    img = draw_boxes_on_character(img)
    cv2.imshow("Character Bounding Boxes", img)

    # draw bounding boxes on full text
    img = draw_boxes_on_text(img)
    cv2.imshow("Text Bounding Boxes", img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()