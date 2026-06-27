FROM python:3.11-slim

# System dependencies: Tesseract OCR + Poppler (needed by pdf2image)
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

COPY . .

RUN chmod +x start.sh
RUN mkdir -p uploads

# Render sets $PORT at runtime; the app must listen on it (handled in start.sh)
EXPOSE 8501

CMD ["./start.sh"]
