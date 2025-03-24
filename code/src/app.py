from flask import Flask, request, render_template, jsonify
import os
import fitz  # PyMuPDF for PDF handling
import re
import requests
import pytesseract
from PIL import Image
from bs4 import BeautifulSoup
import base64
import io

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Google Gemini API Key (Add your own key)
GEMINI_API_KEY = ""
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent"

# Classification Mapping
CLASSIFICATION_MAPPING = {
    "Adjustment": [],
    "AU Transfer": [],
    "Closing Notice": ["Reallocation Fees", "Amendment Fees", "Reallocation Principal"],
    "Commitment Charge": ["Cashless Roll", "Decrease", "Increase"],
    "Fee Payment": ["Ongoing Fee", "Letter of Credit Fee"],
    "Money Movement-Inbound": ["Principal", "Interest", "Principal + Interest", "Principal + Fee + Interest"],
    "Money Movement-Outbound": ["Timebound", "Foreign Currency"]
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process_email():
    try:
        email_html = request.form.get("emailContent")
        files = request.files.getlist("fileUpload")

        extracted_texts = []

        # Process email body
        email_text = extract_text_from_email_body(email_html)
        extracted_texts.append(email_text)

        # Process uploaded files
        for file in files:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            extracted_texts.append(extract_text_from_file(file_path))

        if not any(extracted_texts):
            return jsonify({"error": "No valid email content or attachments provided"}), 400

        full_text = "\n\n".join(filter(None, extracted_texts))
        cleaned_text = preprocess_text(full_text)
        masked_text = mask_pii(cleaned_text)
        keywordsFromEmail = extract_keywords(masked_text)
        classification = classify_email_with_gemini(masked_text)

        return jsonify({
            "classification": classification,
            "keywordsFromEmail": keywordsFromEmail if keywordsFromEmail else {"Request Type": "Unknown"}
        })
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Google Gemini API Error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

def mask_pii(text):
    """Mask sensitive data before sending to LLM"""
    text = re.sub(r"\b\d{4}-\d{4}-\d{4}-\d{4}\b", "[ACCOUNT-NUMBER]", text)  # Mask Account Numbers
    text = re.sub(r"TXN\d+", "[TRANSACTION-ID]", text)  # Mask Transaction IDs
    text = re.sub(r"\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?", "[AMOUNT]", text)  # Mask Monetary Values
    text = re.sub(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}, \d{4}\b", "[DATE]", text)  # Mask Dates
    text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[SSN]", text)  # Mask Social Security Numbers (US)
    text = re.sub(r"\b\d{10,16}\b", "[CARD-NUMBER]", text)  # Mask Card Numbers
    return text


def extract_text_from_file(file_path):
    try:
        if file_path.endswith(".txt") or file_path.endswith(".eml"):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        elif file_path.endswith(".pdf"):
            doc = fitz.open(file_path)
            return "\n".join([page.get_text() for page in doc])
        elif file_path.endswith((".png", ".jpg", ".jpeg")):
            return pytesseract.image_to_string(Image.open(file_path))
        else:
            return "Unsupported file format"
    except Exception as e:
        return f"Error processing file: {str(e)}"

def extract_text_from_email_body(email_html):
    try:
        soup = BeautifulSoup(email_html, "html.parser")
        text = soup.get_text()
        for img in soup.find_all("img"):
            img_src = img.get("src", "")
            if img_src.startswith("data:image"):
                img_data = img_src.split(",")[1]
                image = Image.open(io.BytesIO(base64.b64decode(img_data)))
                text += "\n" + pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        return f"Error processing email body: {str(e)}"

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text

def extract_keywords(text):
    keywords = {}
    patterns = {
        "Amount": r"\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?",
        "Transaction ID": r"TXN\d+",
        "Date": r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}, \d{4}\b",
        "Account Number": r"\b\d{4}-\d{4}-\d{4}-\d{4}\b",
        "Fee Type": r"\b(?:Late Fee|Processing Fee|Service Charge|Penalty)\b"
    }
    for key, pattern in patterns.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            keywords[key] = matches[:3]
    request_type = "Unknown"
    for req, pattern in CLASSIFICATION_MAPPING.items():
        if re.search(rf"\b{req}\b", text, re.IGNORECASE):
            request_type = req
            break
    sub_type_patterns = CLASSIFICATION_MAPPING.get(request_type, [])
    matched_sub_types = [sub for sub in sub_type_patterns if re.search(rf"\b{sub}\b", text, re.IGNORECASE)]
    if not matched_sub_types:
        matched_sub_types.append("No Sub Type Found")
    keywords["Request Type"] = request_type
    keywords["Sub Type"] = matched_sub_types
    return keywords

def classify_email_with_gemini(content):
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    prompt = f"""
    You are an AI trained to classify emails into the following categories:
    {list(CLASSIFICATION_MAPPING.keys())}.
    Given the following email content, classify it under one of the categories above.
    If confidence is low, classify it as 'Edge Case'.
    Email Content:
    {content}
    """
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=data)
    result = response.json()
    if "candidates" in result and result["candidates"]:
        response_text = result["candidates"][0]["content"]["parts"][0]["text"].strip()
        best_match = "Edge Case"
        for category in CLASSIFICATION_MAPPING.keys():
            if category.lower() in response_text.lower():
                best_match = category
                break
        return [{"Request Type": best_match, "Confidence": 0.9, "Request Sub Type": CLASSIFICATION_MAPPING.get(best_match, ["None"])}]
    return [{"Request Type": "Edge Case", "Confidence": 0, "Request Sub Type": "None"}]

if __name__ == "__main__":
    app.run(debug=True)
