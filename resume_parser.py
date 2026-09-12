"""
resume_parser.py
-----------------
Handles reading a resume file (PDF or DOCX) and pulling out plain text
so the rest of the app can analyze it.
"""

import io
from PyPDF2 import PdfReader
import docx


def extract_text_from_pdf(uploaded_file) -> str:
    """Read a PDF file object and return all its text as one string."""
    text = ""
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def extract_text_from_docx(uploaded_file) -> str:
    """Read a DOCX file object and return all its text as one string."""
    document = docx.Document(uploaded_file)
    text = "\n".join(paragraph.text for paragraph in document.paragraphs)
    return text


def extract_text(uploaded_file) -> str:
    """
    Figure out the file type from its name and extract text accordingly.
    `uploaded_file` here is a Streamlit UploadedFile object.
    """
    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif filename.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    else:
        raise ValueError("Unsupported file type. Please upload a PDF or DOCX file.")
