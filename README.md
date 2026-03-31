# 🏥 MedExplain AI — Smart Medical Report Analyzer

> Upload a medical report (PDF or image) → OCR extracts values → AI analyzes risks → Chat about your results.

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Flowchart](#-flowchart)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [API Reference](#-api-reference)
- [AI Risk Logic](#-ai-risk-logic)
- [Tech Stack](#-tech-stack)
- [Troubleshooting](#-troubleshooting)

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 **File Upload** | Drag-and-drop or click to upload PDF / JPG / PNG |
| 🔍 **OCR Extraction** | pytesseract extracts text from images; PyMuPDF reads PDFs |
| 📊 **Value Parsing** | Regex detects Hemoglobin, Glucose, WBC, RBC, Cholesterol, etc. |
| 🚦 **Risk Prediction** | Rule-based + OpenAI flags Anemia, Diabetes, CV risk |
| 🤖 **AI Chat** | GPT-3.5 chatbot answers questions about your specific report |
| 🎨 **Color-coded UI** | Green = normal, Orange = low, Red = high |

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                            │
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐  │
│  │  Upload Page │    │ Results Page │    │   AI Chat UI     │  │
│  │  (Drag&Drop) │───▶│ (Lab Values) │◀──▶│  (ChatGPT-like)  │  │
│  └──────────────┘    └──────────────┘    └──────────────────┘  │
│         │  React + Tailwind CSS (Vanilla HTML or Vite)          │
└─────────┼───────────────────────────────────────────────────────┘
          │  HTTP (multipart/form-data or JSON)
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND (port 8000)                  │
│                                                                 │
│  POST /analyze                    POST /chat                    │
│  ┌──────────────────────────┐    ┌──────────────────────────┐  │
│  │ 1. Receive file upload   │    │ 1. Receive question +    │  │
│  │ 2. Detect PDF or image   │    │    report_data context   │  │
│  │ 3. OCR extraction        │    │ 2. Build GPT prompt      │  │
│  │ 4. Regex value parsing   │    │ 3. Call OpenAI API       │  │
│  │ 5. Risk rule engine      │    │ 4. Return AI answer      │  │
│  │ 6. OpenAI explanation    │    └──────────────────────────┘  │
│  │ 7. Return JSON response  │                                   │
│  └──────────────────────────┘                                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
    ┌──────────┐  ┌──────────┐  ┌──────────────┐
    │pytesseract│  │ PyMuPDF  │  │  OpenAI API  │
    │  (OCR)   │  │  (PDF)   │  │  (GPT-3.5)   │
    └──────────┘  └──────────┘  └──────────────┘
```

---

## 🔄 Flowchart

```
        ┌─────────────┐
        │    START    │
        └──────┬──────┘
               │
               ▼
   ┌─────────────────────┐
   │   User Visits App   │
   └──────────┬──────────┘
              │
              ▼
   ┌─────────────────────┐
   │  Upload PDF/Image   │
   └──────────┬──────────┘
              │
              ▼
   ┌─────────────────────┐      ┌────────────────┐
   │  Detect File Type   │─────▶│ PDF? → PyMuPDF │
   └─────────────────────┘      │ IMG? → Pillow  │
                                └────────┬───────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │  OCR Text Extraction │
                              │    (pytesseract)     │
                              └──────────┬───────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │  Regex Value Parsing │
                              │  Hemoglobin, Glucose,│
                              │  WBC, RBC, Chol...   │
                              └──────────┬───────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │   Risk Calculation   │
                              │  Rule Engine + GPT   │
                              └──────────┬───────────┘
                                         │
                          ┌──────────────┼──────────────┐
                          ▼              ▼              ▼
                     ┌─────────┐  ┌──────────┐  ┌──────────┐
                     │LOW RISK │  │MED RISK  │  │HIGH RISK │
                     │(green)  │  │(orange)  │  │(red)     │
                     └────┬────┘  └────┬─────┘  └────┬─────┘
                          └────────────┼──────────────┘
                                       │
                                       ▼
                              ┌──────────────────────┐
                              │  Display Results UI  │
                              │  + AI Explanation    │
                              └──────────┬───────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │   AI Chat Session    │◀─── User Questions
                              │  (GPT-3.5 context)   │
                              └──────────┬───────────┘
                                         │
                                         ▼
                                    ┌─────────┐
                                    │   END   │
                                    └─────────┘
```

---

## 📁 Project Structure

```
medexplain/
│
├── frontend/
│   └── index.html              ← Complete single-file frontend (React + Tailwind)
│                                  Open directly in browser, no build step needed!
│
├── backend/
│   ├── main.py                 ← FastAPI application (all routes + logic)
│   ├── requirements.txt        ← Python dependencies
│   └── .env.example            ← Copy to .env and add your OpenAI key
│
└── README.md                   ← This file
```

### Optional Vite/React project structure (for production):

```
frontend/
├── src/
│   ├── components/
│   │   ├── ValueRow.jsx        ← Lab value display with bar chart
│   │   ├── Chat.jsx            ← AI chat interface
│   │   └── RiskBadge.jsx       ← Color-coded risk indicator
│   ├── pages/
│   │   ├── Upload.jsx          ← Home / upload page
│   │   └── Results.jsx         ← Analysis results page
│   ├── App.jsx                 ← Router + state management
│   └── main.jsx                ← Vite entry point
├── index.html
├── tailwind.config.js
└── package.json
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+ (optional — only needed for Vite build)
- Tesseract OCR installed on your system
- An OpenAI API key

### Step 1 — Install Tesseract OCR

**macOS:**
```bash
brew install tesseract
```

**Ubuntu / Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**Windows:**
Download and install from:
https://github.com/UB-Mannheim/tesseract/wiki

Then add to PATH: `C:\Program Files\Tesseract-OCR`

### Step 2 — Backend Setup

```bash
# 1. Navigate to backend folder
cd medexplain/backend

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set your OpenAI API key
cp .env.example .env
# Edit .env and paste your key:
# OPENAI_API_KEY=sk-your-actual-key-here

# 6. Run the server
uvicorn main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

Visit http://localhost:8000 to verify the API is running.

### Step 3 — Frontend Setup

**Option A — Zero build (recommended for beginners):**

Simply open `frontend/index.html` in your browser. It uses React via CDN.

> ⚠️ Some browsers block local CORS requests. If you see errors, serve it:
> ```bash
> cd medexplain/frontend
> python -m http.server 3000
> ```
> Then open: http://localhost:3000

**Option B — Vite (for development with hot-reload):**

```bash
cd medexplain/frontend
npm create vite@latest . -- --template react
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
npm install
npm run dev
```

Then replace `src/App.jsx` with the component logic from `index.html`.

---

## 📡 API Reference

### `POST /analyze`

Analyzes an uploaded medical report file.

**Request:** `multipart/form-data`
- `file`: PDF, JPG, or PNG file

**Response:**
```json
{
  "raw_text": "LABORATORY REPORT...",
  "values": {
    "hemoglobin": {
      "value": 10.5,
      "unit": "g/dL",
      "status": "low",
      "normal_range": "12.0 – 17.5"
    },
    "glucose": {
      "value": 156.0,
      "unit": "mg/dL",
      "status": "high",
      "normal_range": "70.0 – 100.0"
    }
  },
  "risk": {
    "level": "High",
    "risks": [
      {
        "condition": "Anemia",
        "severity": "medium",
        "reason": "Hemoglobin 10.5 g/dL is below normal range"
      },
      {
        "condition": "Diabetes Risk",
        "severity": "high",
        "reason": "Glucose 156.0 mg/dL is significantly elevated"
      }
    ]
  },
  "explanation": "Your hemoglobin is slightly low, which may indicate anemia..."
}
```

---

### `POST /chat`

Chat with AI about your report.

**Request:** `application/json`
```json
{
  "question": "Should I be worried about my glucose level?",
  "report_data": {
    "values": { ... },
    "risk": { ... },
    "explanation": "..."
  }
}
```

**Response:**
```json
{
  "answer": "Your glucose of 156 mg/dL is above the normal fasting range of 70–100 mg/dL. This may indicate pre-diabetes or diabetes. I strongly recommend scheduling an appointment with your doctor for an HbA1c test. In the meantime, reducing sugary foods and increasing physical activity can help. Always consult your doctor for a proper diagnosis."
}
```

---

## 🤖 AI Risk Logic

### Detected Biomarkers

| Biomarker | Normal Range | Low Risk Condition | High Risk Condition |
|---|---|---|---|
| Hemoglobin | 12.0–17.5 g/dL | Anemia (below 12) | — |
| Glucose | 70–100 mg/dL | Pre-Diabetes (100–140) | Diabetes Risk (>140) |
| WBC | 4.5–11.0 K/μL | Immune Concern | Infection/Inflammation |
| RBC | 4.2–5.9 M/μL | Low RBC count | — |
| Platelets | 150–400 K/μL | Thrombocytopenia | Thrombocytosis |
| Cholesterol | 0–200 mg/dL | — | Cardiovascular Risk |
| Creatinine | 0.6–1.2 mg/dL | — | Kidney Concern |
| Sodium | 136–145 mEq/L | Hyponatremia | Hypernatremia |
| Potassium | 3.5–5.0 mEq/L | Hypokalemia | Hyperkalemia |

### Risk Level Calculation

```
Any value = HIGH severity  →  Overall Risk = High
All values = MEDIUM severity  →  Overall Risk = Medium
No abnormal values  →  Overall Risk = Low
```

### OCR Regex Patterns

The backend uses case-insensitive regex to find values like:

```
Hemoglobin: 10.5
HGB : 10.5
HB: 10.5
Glucose: 156 mg/dL
Blood Sugar: 156
Fasting Glucose: 156
```

---

## 🛠 Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | React 18 | UI components and state |
| Styling | Tailwind CSS / Custom CSS | Responsive, clean design |
| Backend | FastAPI (Python) | REST API server |
| OCR | pytesseract + Pillow | Image → Text |
| PDF | PyMuPDF (fitz) | PDF → Text |
| AI (Explain) | OpenAI GPT-3.5 | Natural language explanation |
| AI (Chat) | OpenAI GPT-3.5 | Context-aware Q&A |
| Risk Logic | Python rule engine | Biomarker thresholds |
| Server | Uvicorn (ASGI) | ASGI server for FastAPI |

---

## 🔧 Troubleshooting

### "CORS error" in browser console
Make sure the FastAPI server is running on port 8000. CORS is configured to allow `localhost:3000` and `localhost:5173`.

### "TesseractNotFoundError"
Tesseract is not installed or not in your PATH. See Step 1 above.

### "openai.AuthenticationError"
Your OpenAI API key is missing or invalid. Edit `backend/.env` and add your key. The app will still work without a key (falls back to rule-based explanations), but chat responses will be generic.

### "No values detected"
The report text may be too faint, rotated, or use non-standard formatting. Try:
- A higher-resolution scan
- Straightening the image
- Using a text-based PDF instead of a scanned image

### "Module not found: fitz"
Run: `pip install PyMuPDF`

### Backend returns 422 Unprocessable Entity
The file type is not supported. Only `image/jpeg`, `image/png`, and `application/pdf` are accepted.

---

## 🔐 Privacy Note

- Files are processed in-memory and are **not saved to disk or any database**.
- Raw text is truncated to 500 characters in the API response.
- If you need persistent storage, add MongoDB with `motor` (async MongoDB driver) and store anonymized reports.

---

## 📝 Sample Test Report

To test without a real report, create a text file with this content, print it, and photograph it (or convert to PDF):

```
LABORATORY REPORT
Patient Name: John Doe
Date: 2024-01-15

COMPLETE BLOOD COUNT
Hemoglobin (HGB): 10.2 g/dL       [Reference: 12.0-17.5]
WBC: 12.5 K/uL                     [Reference: 4.5-11.0]
RBC: 3.8 M/uL                      [Reference: 4.2-5.9]
Platelets: 180 K/uL                 [Reference: 150-400]

METABOLIC PANEL
Glucose: 162 mg/dL                  [Reference: 70-100]
Sodium: 140 mEq/L                   [Reference: 136-145]
Potassium: 4.1 mEq/L               [Reference: 3.5-5.0]
Creatinine: 0.9 mg/dL              [Reference: 0.6-1.2]

LIPID PANEL
Total Cholesterol: 225 mg/dL        [Reference: < 200]
```

This will trigger: Anemia (low HGB), Diabetes Risk (high glucose), Cardiovascular Risk (high cholesterol), and WBC elevation — giving a **High** risk result for demonstration.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## ⚠️ Disclaimer

MedExplain AI is an educational tool only. It is **not** a medical device, does **not** provide medical advice, and is **not** a substitute for professional medical consultation. Always consult a qualified healthcare provider for diagnosis and treatment decisions.

---

*Built with ❤️ using FastAPI, React, pytesseract, and OpenAI*
