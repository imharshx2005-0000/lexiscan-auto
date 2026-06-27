from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import uuid

from utils import extract_text_from_pdf, validate_entities
from ner_model import extract_entities

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return {"message": "LexiScan Auto API Running 🚀"}


@app.route("/process", methods=["POST"])
def process_document():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF files are supported"}), 400

    # Prefix with a uuid so concurrent/duplicate filenames never collide or overwrite
    safe_name = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
    file_path = os.path.join(UPLOAD_FOLDER, safe_name)
    file.save(file_path)

    try:
        text = extract_text_from_pdf(file_path)
        entities = extract_entities(text)
        validated_entities = validate_entities(entities)
    finally:
        # Clean up the uploaded file regardless of success/failure
        if os.path.exists(file_path):
            os.remove(file_path)

    return jsonify({
        "text_sample": text[:1000],
        "entities": validated_entities
    })


if __name__ == "__main__":
    # Internal sidecar process — only reachable from inside the same container,
    # so binding to localhost only (not 0.0.0.0) is intentional and safer.
    port = int(os.environ.get("FLASK_INTERNAL_PORT", 5000))
    app.run(host="127.0.0.1", port=port, debug=False)