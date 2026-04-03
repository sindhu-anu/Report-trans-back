# utils.py

import re
import io
import os
from PIL import Image
import google.generativeai as genai

# -------------------------------
# GEMINI CONFIG
# -------------------------------
genai.configure(api_key="AIzaSyDwbKrtExUpoQjs4oiJVqR2pQyqZTGfgf4")
model = genai.GenerativeModel("gemini-2.5-flash")


# -------------------------------
# GEMINI OCR FUNCTION
# -------------------------------
import time

def call_gemini_ocr(image_bytes):

    image = Image.open(io.BytesIO(image_bytes))

    prompt = """
    You are a medical lab report parser.

    Extract values and return STRICT JSON:

    {
      "Hb": number or null,
      "WBC": number or null,
      "Platelets": number or null,
      "PT": number or null,
      "INR": number or null
    }

    Rules:
    - Return ONLY JSON
    - No explanation
    - If not found, use null
    """

    response = model.generate_content([prompt, image])

    return response.text
# -------------------------------
# CLEAN TEXT
# -------------------------------
def clean_text(text):
    text = text.replace("\n", " ")
    text = text.replace(":", " ")
    text = text.replace(",", " ")
    return text.strip()


# -------------------------------
# EXTRACT VALUES
# -------------------------------
def extract_values(text):
    data = {}

    hb = re.search(r'(Hb|Haemoglobin|Hemoglobin)\s*(\d+\.?\d*)', text, re.I)
    wbc = re.search(r'(WBC|Total W\.?B\.?C\.?|Total Leucocyte Count)\s*(\d+)', text, re.I)
    platelets = re.search(r'(Platelet Count|Platelets?)\s*(\d+)', text, re.I)
    pt = re.search(r'(PT|PATIENT VALUE)\s*(\d+)', text, re.I)
    inr = re.search(r'(INR)\s*(\d+\.?\d*)', text, re.I)

    if hb: data["Hb"] = hb.group(2)
    if wbc: data["WBC"] = hb and wbc.group(2)
    if platelets: data["Platelets"] = platelets.group(2)
    if pt: data["PT"] = pt.group(2)
    if inr: data["INR"] = inr.group(2)

    return data


# -------------------------------
# CORRECT VALUES
# -------------------------------
def correct_values(data):

    if "WBC" in data and data["WBC"]:
        wbc = int(data["WBC"])
        if wbc < 1000:
            data["WBC"] = str(wbc * 10)

    if "Hb" in data and data["Hb"]:
        hb = float(data["Hb"])
        if hb > 25:
            data["Hb"] = str(hb / 10)

    return data


# -------------------------------
# FORMAT OUTPUT
# -------------------------------
def convert_value(val):
    if val is None or val == "NA":
        return None
    try:
        return float(val) if "." in str(val) else int(val)
    except:
        return val


def format_output(data):
    return {
        "Hb": convert_value(data.get("Hb")),
        "WBC": convert_value(data.get("WBC")),
        "Platelets": convert_value(data.get("Platelets")),
        "PT": convert_value(data.get("PT")),
        "INR": convert_value(data.get("INR"))
    }


# -------------------------------
# FINAL API FORMAT
# -------------------------------
def prepare_api_response(outputs):

    reports = []

    for i, report in enumerate(outputs, start=1):
        reports.append({
            "report_id": i,
            "tests": report
        })

    return {
        "status": "success",
        "reports": reports
    }