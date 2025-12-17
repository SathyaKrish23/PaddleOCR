import os
import warnings
import logging
import time
import numpy as np
import cv2
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
# --- 1. CONFIGURATION MUST BE AT THE VERY TOP ---
os.environ["DISABLE_MODEL_SOURCE_CHECK"] = "True"
os.environ["PADDLE_MODEL_OFFLINE"] = "1"
os.environ["FLAGS_minloglevel"] = "3"
os.environ["GLOG_minloglevel"] = "3"

from paddleocr import PaddleOCR # Import after setting env vars

warnings.filterwarnings("ignore")
logging.getLogger("ppocr").setLevel(logging.ERROR)
logging.getLogger("paddle").setLevel(logging.ERROR)

# --- 2. PADDLEOCR INITIALIZATION (MAX SPEED FOR CPU) ---
try:
    # ⚡️ Configuration: Maximum CPU speed (MKLDNN) and stability (no extra params)
    ocr = PaddleOCR(
        use_angle_cls=False,      # Skip angle orientation check (faster)
        lang='en',                # Use the fast English model
        enable_mkldnn=True,       # CRITICAL for maximum CPU speed
    )
    print("🚀 PaddleOCR initialized successfully. (Final stable configuration active)")
except Exception as e:
    print(f"CRITICAL ERROR initializing PaddleOCR: {e}")
    ocr = None

# --- 3. THREAD POOL FOR NON-BLOCKING ASYNC ---
executor = ThreadPoolExecutor(max_workers=os.cpu_count() or 4)

app = FastAPI()

ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/tiff", "image/bmp"}

# --- HELPER: IN-MEMORY PROCESSING (CRITICAL FIX HERE) ---
def run_ocr_on_bytes(file_bytes: bytes, filename: str) -> Dict[str, Any]:
    start = time.time()
    if ocr is None:
        return {"extracted_text_lines": [], "message": "OCR service down."}

    try:
        # A. Decode bytes to numpy array
        nparr = np.frombuffer(file_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return {"extracted_text_lines": [], "message": "Could not decode image data."}

        # B. Run OCR (FIX: Explicitly request a more robust detection model)
        # Using the standard model names ensures better detection accuracy.
        result = ocr.ocr(img)
        data = result[0]["rec_texts"] if result[0]["rec_texts"]  else []
        process_time = round(time.time() - start, 4)

        return {"OCR-Time":process_time, "data": data}

    except Exception as e:
        logging.error(f"Error processing {filename}: {e}")
        return {
            "extracted_text_lines": [],
            "message": f"Processing failed: {str(e)}"
        }

# --- 4. FASTAPI ENDPOINT (Unchanged) ---
@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    start = time.time()

    if file.content_type not in ALLOWED_MIME_TYPES:
        return JSONResponse(status_code=400, content={"message": "Invalid file type. Only standard images are supported."})

    # If initialization failed, return 503 early
    if ocr is None:
         return JSONResponse(status_code=503, content={"message": "OCR service not initialized."})

    try:
        file_bytes = await file.read()
    except Exception:
         return JSONResponse(status_code=400, content={"message": "File read error."})

    # Run heavy task in background thread
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(executor, run_ocr_on_bytes, file_bytes, file.filename)

    process_time = time.time() - start
    print(f"OCR Time: {process_time:.4f}s")
    
    return JSONResponse(content=result)