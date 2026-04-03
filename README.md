📄 AI-Powered Medical OCR Backend

This project is a FastAPI backend that uses Google Gemini AI to extract structured medical data from lab reports.

🚀 Features
📷 Image upload (lab reports / prescriptions)
🤖 Gemini OCR integration
📊 Structured JSON output
⚡ FastAPI backend (ready for deployment)
📦 Tech Stack
FastAPI
Google Gemini API
Python
Pillow
🔧 API Endpoint
POST /process

Upload an image and get extracted values.

Response:
{
  "status": "success",
  "reports": [
    {
      "report_id": 1,
      "tests": {
        "Hb": 13.5,
        "WBC": 5000,
        "Platelets": 200000,
        "PT": null,
        "INR": null
      }
    }
  ]
}
▶️ Run Locally
pip install -r requirements.txt
python -m uvicorn main:app --reload
🔐 Environment Variable

Set your API key:

set GOOGLE_API_KEY=your_key
