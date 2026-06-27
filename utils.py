import pytesseract
from pdf2image import convert_from_path
import re
import os

# Local Windows paths — only used if these env vars are set.
# On Render/Linux/Docker, Tesseract and Poppler are installed via apt
# and already on PATH, so these are left unset there and have no effect.
TESSERACT_CMD = os.environ.get("TESSERACT_CMD")
POPPLER_PATH = os.environ.get("POPPLER_PATH")

if TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD


def extract_text_from_pdf(pdf_path):
    if POPPLER_PATH:
        images = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
    else:
        images = convert_from_path(pdf_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)
    return text
def validate_entities(entities):
    validated = []

    for ent in entities:
        label = ent['label']
        value = ent['text']
        if label == "DATE":
            if re.match(r"\d{4}-\d{2}-\d{2}", value):
                validated.append(ent)

        elif label == "MONEY":
            if re.search(r"\$|₹|€", value):
                validated.append(ent)

        else:
            validated.append(ent)
    return validated
