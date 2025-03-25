# 🚀 Project Name

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction
In today's digital world, emails contain a wealth of sensitive information, including personally identifiable information (PII) and confidential data. Ensuring the safe processing of such emails before leveraging AI models is crucial to maintaining privacy and compliance.

This project is designed to intelligently analyze email content, identify and redact PII or sensitive data, and then process the refined content using Gemini AI for classification. By doing so, we aim to enhance security, ensure data privacy, and leverage AI for insightful email categorization without exposing sensitive details.

This solution is particularly useful for organizations handling large volumes of emails, ensuring that AI models receive only sanitized data while maintaining the integrity and intent of the content.

## 🎥 Demo
🔗 [Live Demo](#) (if applicable)  
📹 [Video Demo](https://github.com/ewfx/gaied-ai-explorers/blob/main/artifacts/demo/Email%20Extraction.mp4)
🖼️ Screenshots:

![Screenshot 1](https://github.com/ewfx/gaied-ai-explorers/blob/main/artifacts/demo/Email%20Classifier%20Screenshot-1.png)
![Screenshot 2](https://github.com/ewfx/gaied-ai-explorers/blob/main/artifacts/demo/Email%20Classifier%20Screenshot-2.png)

## 💡 Inspiration
With the increasing reliance on AI for email processing and classification, we noticed a major challenge—how to ensure sensitive information, like PII, is handled securely before being fed into large language models. Many organizations struggle with balancing AI automation and data privacy, especially when dealing with high volumes of emails containing confidential details.

We wanted to take on this challenge while also stepping out of our comfort zone. Coming from a Dynamics 365 background, we’ve been hearing so much buzz about Python, and this project felt like the perfect opportunity to explore cutting-edge technologies. By leveraging Python, we aimed to build a smart, efficient, and privacy-conscious solution that can help organizations safely process and classify emails without compromising sensitive data.

## ⚙️ What It Does
- ✅ Extract text from email bodies, PDFs, images, and text files for deeper analysis.
- ✅ Analyze structured data, including transaction IDs, dates, and financial details, to derive meaningful insights.
- ✅ Classify emails using Google Gemini AI for smart and efficient categorization.
- ✅ Process inline images with OCR to capture critical details often embedded in screenshots.
- ✅ Enhance accuracy through regex-based keyword extraction, ensuring precise identification of key data points.

## 🛠️ How We Built It
-🔹 Python – Used for data processing, text extraction, and automation.
-🔹 Google Gemini AI – Powers the intelligent classification of email content.
-🔹 OCR (Optical Character Recognition) – Extracts text from images and scanned documents.
-🔹 Regex (Regular Expressions) – Helps in structured data extraction, such as transaction IDs and key phrases.
-🔹 Email Parsing Libraries – Used to process .eml files and extract relevant content.

## 🚧 Challenges We Faced
- 🚧 Handling Diverse Email Formats – Emails come in various formats (.eml, plain text, HTML), making consistent data extraction tricky.
- 🚧 Extracting Text from Inline Images – Many emails include screenshots instead of text, requiring OCR for accurate extraction.
- 🚧 Identifying and Masking PII – Ensuring personally identifiable information (PII) was detected and handled securely before processing.
- 🚧 Optimizing AI Prompts – Fine-tuning prompts for Google Gemini AI to improve classification accuracy and relevance.
- 🚧 Regex Complexity – Crafting regex patterns to extract structured data while minimizing false positives.
- 🚧 Exploring a New Tech Stack – Coming from a Dynamics 365 background, learning and implementing Python, OCR, and AI models was a challenge, but it was an exciting opportunity to work with cutting-edge technologies.

## 🏃 How to Run
1. Clone the repository  
   ```sh
   git clone [https://github.com/your-repo.git](https://github.com/ewfx/gaied-ai-explorers)
   ```
2. Install dependencies  
   ```sh
   npm install  # or pip install -r requirements.txt (for Python)
   ```
3. Run the project  
   ```sh
   npm start  # or python app.py
   ```

## 🏗️ Tech Stack
- 🔹 Frontend: HTML/ JavaScript
- 🔹 Backend: Python
- 🔹 OCR Processing: Tesseract OCR  
- 🔹 Other: Google Gemini AI / Tesseract OCR / RegEx

## 👥 Team
- **Your Name** - [GitHub](#) | [LinkedIn](#)
- **Teammate 2** - [GitHub](#) | [LinkedIn](#)
