# main.py

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import json

from utils import call_gemini_ocr, prepare_api_response

app = FastAPI()

# -------------------------------
# CORS (allow frontend access)
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# HOME ROUTE
# -------------------------------
@app.get("/")
def home():
    return {"message": "Backend running"}

# -------------------------------
# MAIN PROCESS API
# -------------------------------
@app.post("/process")
async def process(file: UploadFile = File(...)):

    try:
        # 1. Read uploaded image
        content = await file.read()

        # 2. Call Gemini OCR (returns JSON string)
        text = call_gemini_ocr(content)

        # 3. Clean response (important)
        text = text.strip()
        text = text.replace("```json", "").replace("```", "")

        # 4. Convert JSON string → Python dict
        try:
            data = json.loads(text)
        except:
            data = {
                "Hb": None,
                "WBC": None,
                "Platelets": None,
                "PT": None,
                "INR": None
            }

        # 5. Wrap for UI
        response = prepare_api_response([data])

        return response

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }