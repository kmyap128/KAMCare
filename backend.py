from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import pytesseract
from google.cloud import vision
import io
import requests

app = FastAPI()

# Initialize Google Vision API client
vision_client = vision.ImageAnnotatorClient()

# RxNorm API base URL (for medication lookup)
RXNORM_API = "https://rxnav.nlm.nih.gov/REST/rxcui.json?name="

def extract_text_google_vision(image_bytes: bytes):
    image = vision.Image(content=image_bytes)
    response = vision_client.text_detection(image=image)
    texts = response.text_annotations
    if texts:
        return texts[0].description.strip()
    return ""

def extract_text_tesseract(image_bytes: bytes):
    return pytesseract.image_to_string(io.BytesIO(image_bytes)).strip()

def get_medication_info(med_name: str):
    response = requests.get(RXNORM_API + med_name)
    if response.status_code == 200:
        data = response.json()
        if "idGroup" in data and "rxnormId" in data["idGroup"]:
            return {"rxnormId": data["idGroup"]["rxnormId"]}
    return {"error": "Medication not found"}

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    
    # Try extracting text with Google Vision API
    extracted_text = extract_text_google_vision(image_bytes)
    
    if not extracted_text:
        # Fallback to Tesseract OCR
        extracted_text = extract_text_tesseract(image_bytes)
    
    if not extracted_text:
        return JSONResponse(content={"error": "No text detected."}, status_code=400)
    
    # Lookup medication info
    med_info = get_medication_info(extracted_text)
    
    return JSONResponse(content={"medication": extracted_text, "info": med_info})
