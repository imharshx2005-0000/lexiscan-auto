import streamlit as st
import requests
import os
import html

# Flask runs as an internal sidecar process inside the same container,
# so this stays localhost even in production on Render.
BACKEND_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:5000")

st.set_page_config(
    page_title="LexiScan Auto",
    page_icon="🤖",
    layout="wide"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    border: none;
}

.card {
    background-color: #1E1E1E;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    color: white;
}

h1, h2, h3, h4 {
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.title("🤖 LexiScan Auto")

menu = st.sidebar.radio(
    "Navigation",
    ["Upload & Process", "About"]
)

# ---------- HEADER ----------
st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>📄 Intelligent Document Processing</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center;'>Upload legal documents & extract key entities instantly</p>",
    unsafe_allow_html=True
)

# ---------- MAIN ----------
if menu == "Upload & Process":

    st.markdown("### 📤 Upload PDF")

    uploaded_file = st.file_uploader(
        "Upload Contract PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:

        st.success(f"✅ File Uploaded: {uploaded_file.name}")

        if st.button("🚀 Process Document"):

            with st.spinner("Processing document..."):

                try:

                    response = requests.post(
                        f"{BACKEND_URL}/process",
                        files={
                            "file": (
                                uploaded_file.name,
                                uploaded_file,
                                "application/pdf"
                            )
                        },
                        timeout=120
                    )

                    if response.status_code == 200:

                        data = response.json()

                        st.success("✅ Processing Complete!")

                        # ---------- TEXT PREVIEW ----------
                        st.markdown("### 📄 Extracted Text Preview")

                        st.markdown(
                            f"""
                            <div class='card'>
                            {html.escape(data['text_sample']).replace(chr(10), '<br>')}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        # ---------- ENTITIES ----------
                        st.markdown("### 🧠 Extracted Entities")

                        if len(data["entities"]) == 0:
                            st.warning("No entities detected.")

                        for ent in data["entities"]:

                            st.markdown(
                                f"""
                                <div class='card'>
                                <b>Text:</b> {html.escape(ent['text'])} <br><br>
                                <b>Label:</b> {html.escape(ent['label'])}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                    else:
                        st.error("❌ API Error")

                except requests.exceptions.Timeout:
                    st.error("❌ The document took too long to process. Try a smaller file.")
                except Exception as e:
                    st.error(f"❌ Connection Error: {e}")

# ---------- ABOUT ----------
elif menu == "About":

    st.markdown("""
    ## 📌 About Project

    **LexiScan Auto** is an AI-powered Intelligent Document Processing system.

    ### 🚀 Features
    - OCR-based text extraction
    - Named Entity Recognition (NER)
    - Legal document analysis
    - Structured JSON response
    - Premium Streamlit Dashboard

    ### 🧠 Technologies Used
    - Python
    - Flask
    - Streamlit
    - spaCy
    - Tesseract OCR
    - pdf2image

    ### 🎯 Use Case
    Automates legal contract processing and entity extraction.
    """)