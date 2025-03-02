import cv2
import pytesseract
from PIL import Image
import numpy as np
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


def openImage(imageName):
    file_path = "image/" + imageName
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Image file '{file_path}' not found!")
    return Image.open(file_path)


# removes trademark and registered symbols: ™, ®
def clean_text(text):
    text = re.sub(r"[™®]", "", text)        # remove trademark & registered symbols
    # text = re.sub(r"[ \t]+", " ", text)     # replace multiple spaces with a single space
    # return text.strip()                     # keeps new lines but remove leading/trailing spaces
    return text

def processImage(img):
    # Convert PIL image to OpenCV format
    img_cv = np.array(img)
    img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    
    # reduces noise
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply OTSU thresholding: changges the image to binary (heavy contrast black/white)
    thresh1 = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 10
    )

    # Specify structure shape and kernel size for dilation
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

    # Find contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Copy image to draw rectangles
    im2 = img_cv.copy()
    extracted_text = []

    # Apply OCR to the full image first (before drawing boxes)
    text = pytesseract.image_to_string(gray).strip()
    cleaned_text = clean_text(text)



    print(cleaned_text)



    if cleaned_text:
        extracted_text.append(cleaned_text)

    # Draw bounding boxes around detected text regions
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green box

    # Write extracted text to file

    if extracted_text:
        with open("recognized.txt", "w") as file:
            file.write("\n".join(extracted_text))


    # Display the image with bounding boxes around text
    cv2.imshow("gray", thresh1)
    cv2.waitKey(0)  # Wait for a key press to close the window
    cv2.destroyAllWindows()  # Close the image window
    

if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = detectTesseract()
    imageName = input("Enter Image Name with Exension (imageName.png): ")
    img = openImage(imageName)
    processImage(img)
