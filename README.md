# GenAI Resume Analysis

A Python and AI-powered project that analyzes resumes to extract skills, experience, and provides recommendations using Google Gemini AI.

---

## 🔹 Project Description

This project allows users to upload resumes and get an AI-based analysis of the candidate’s skills, experience, and suggested improvements. It uses Google Gemini AI for parsing and generating insights. The project is built using Python (Flask), HTML templates, and optionally a database for storing results.

---

## 🔹 Features

- Resume parsing (PDF, DOCX, or text)
- Skill extraction and experience summary
- AI-generated recommendations
- Simple web interface with Flask
- Environment-based configuration using `.env`

---

## 🔹 Folder Structure

genai_resume_analysis/
│
├─ run.py # Main Python file to run the project
├─ requirements.txt # Python dependencies
├─ blueprints/ # Contains Flask routes and templates
│ ├─ Resume_analyse/
│ ├─ routes.py
│ ├─ pycache/
│ └─ template/
│ └─ checker.html
├─ .gitignore # To ignore .env and other unnecessary files
└─ README.md # Project documentation


---

## 🔹 Prerequisites

- Python 3.10+
- pip installed
- Google Gemini API key or other AI API keys

---

## 🔹 Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/PrajwalItnal/genai_resume_analysis.git
cd genai_resume_analysis

2.Create a virtual environment (recommended)
python -m venv venv
# Activate
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

3.Install dependencies
pip install -r requirements.txt

4.Create a .env file in the root directory with your API keys:
GEMINI_API_KEY=your_api_key_here

5.Run the project
python run.py

6.Open the browser at:
http://127.0.0.1:5000