# 📄 LexiScan Auto - Intelligent Document Processing System

LexiScan Auto is an AI-powered document processing system that extracts text from PDF documents using OCR and identifies important entities using Natural Language Processing (NLP).

---

## 🚀 Features

- 📤 Upload PDF documents
- 🔍 OCR-based text extraction using Tesseract
- 🧠 Named Entity Recognition (NER) using spaCy
- ✅ Entity validation using rule-based processing
- 📊 Interactive Streamlit Dashboard
- ⚡ Flask REST API Backend
- 📑 Extract Dates, Organizations, Persons, Locations, Money, and more
- 🐳 Single-container deployment (Docker) — one URL, no separate backend hosting needed

---

## 🏗️ System Architecture

```text
PDF Upload
   ↓
OCR (Tesseract)
   ↓
Text Extraction
   ↓
spaCy NER Model
   ↓
Entity Validation
   ↓
Structured Output
```

The Flask API and Streamlit dashboard run together inside a single Docker container. Streamlit is the public-facing process; Flask runs as an internal sidecar process that Streamlit talks to over `localhost`. This means the whole app deploys as **one service with one URL**.

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend
- Flask

### OCR
- Tesseract OCR

### NLP
- spaCy
- en_core_web_sm Model

### PDF Processing
- pdf2image
- Pillow

### Containerization
- Docker

### Language
- Python

---

## 📂 Project Structure

```text
lexiscan-auto/
│
├── app.py              # Flask backend (OCR + NER API)
├── streamlit_app.py     # Streamlit frontend (dashboard)
├── utils.py             # PDF text extraction + entity validation
├── ner_model.py         # spaCy NER wrapper
├── requirements.txt     # Python dependencies
├── Dockerfile           # Builds the container (installs Tesseract, Poppler, deps)
├── start.sh              # Starts Flask (background) + Streamlit (foreground)
├── .dockerignore
├── uploads/              # Temporary storage for uploaded PDFs (cleaned up after processing)
├── README.md
└── .gitignore
```

---

## ▶️ Running Locally with Docker (recommended)

This mirrors exactly what runs in production, so it's the most reliable way to test changes before deploying.

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

### Step 1: Build the image

```bash
docker build -t lexiscan-test .
```

This installs Tesseract OCR, Poppler, all Python dependencies, and downloads the spaCy model inside the image — no manual installation needed on your machine.

### Step 2: Run the container

```bash
docker run -p 8501:8501 -e PORT=8501 lexiscan-test
```

### Step 3: Open the app

Go to [http://localhost:8501](http://localhost:8501) in your browser.

> If port 8501 is already in use, map to a different local port:
> ```bash
> docker run -p 8502:8501 -e PORT=8501 lexiscan-test
> ```
> and open `http://localhost:8502` instead.

---

## ⚙️ Running Locally without Docker (manual setup)

Only needed if you specifically want to run Flask and Streamlit as separate local processes instead of using Docker.

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/lexiscan-auto.git
cd lexiscan-auto
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
```

Activate Environment

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Step 4: Install Tesseract OCR

Download and install: https://github.com/UB-Mannheim/tesseract/wiki

Verify installation:
```bash
tesseract --version
```

### Step 5: Install Poppler

Download: https://github.com/oschwartz10612/poppler-windows/releases/

Extract to `C:\poppler` (or any path you prefer).

### Step 6: Point the app at your local Tesseract/Poppler installs

Set these environment variables before running (no code changes needed):

```bash
set TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
set POPPLER_PATH=C:\poppler\poppler-26.02.0\Library\bin
```

### Step 7: Run the two processes

Terminal 1 (Flask backend):
```bash
python app.py
```
Expected output: `Running on http://127.0.0.1:5000`

Terminal 2 (Streamlit dashboard):
```bash
streamlit run streamlit_app.py
```

---

## ☁️ Deploying to Render

This project is set up to deploy as a **single Render Web Service** using the included `Dockerfile`.

### Step 1: Push to GitHub

Make sure `Dockerfile`, `start.sh`, and `.dockerignore` are committed alongside the rest of the project files.

### Step 2: Create the service on Render

1. Go to [render.com](https://render.com) → **New +** → **Web Service**
2. Connect your GitHub repo
3. Render should auto-detect the `Dockerfile` (Runtime: Docker). If asked, select Docker explicitly
4. Leave **Build Command** and **Start Command** blank — the Dockerfile's `CMD ["./start.sh"]` handles startup
5. Choose a plan (Free tier works, but OCR may be slower)
6. Click **Create Web Service**

### Step 3: Wait for the build

The first build takes 5–10 minutes since it installs Tesseract, Poppler, and the spaCy model from scratch. In the **Logs** tab, you're looking for:

```text
Running on http://127.0.0.1:5000
You can now view your Streamlit app in your browser
```

### Step 4: Open your live app

Render provides a single public URL (e.g. `https://lexiscan-auto.onrender.com`) — that's the whole app, frontend and backend included.

---

## 📸 Application Workflow

1. Upload PDF Document
2. Convert PDF Pages to Images
3. Extract Text Using OCR
4. Detect Entities Using spaCy
5. Validate Extracted Entities
6. Display Results on Dashboard

---

## 📊 Sample Extracted Entities

| Entity | Label |
|----------|----------|
| John Doe | PERSON |
| Microsoft | ORG |
| New York | GPE |
| ₹50,000 | MONEY |
| 2025-01-01 | DATE |

---

## 🎯 Use Cases

- Legal Contract Analysis
- Agreement Processing
- Invoice Data Extraction
- Compliance Verification
- Document Digitization

---

## 🔮 Future Enhancements

- Multi-language OCR
- PDF Summarization
- AI-based Risk Analysis
- Clause Detection
- Database Integration
- Splitting Flask and Streamlit into independent services for better fault isolation

---

## 👨‍💻 Author

Shikha Singh

Harsh Thakur

### Skills

- Python Development
- Machine Learning
- Natural Language Processing
- Full Stack Development
- AI Applications

---

## 📜 License

This project is developed for educational and learning purposes.
