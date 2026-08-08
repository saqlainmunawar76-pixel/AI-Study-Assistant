"""
utils/documents.py
Extracts plain text from uploaded study documents (PDF, DOCX, TXT).
"""

import io


def extract_text(uploaded_file):
    """
    Takes a Streamlit UploadedFile and returns extracted plain text.
    Supports .txt, .pdf, .docx
    """
    name = uploaded_file.name.lower()

    if name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8", errors="ignore")

    if name.endswith(".pdf"):
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(uploaded_file.read()))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        return text

    if name.endswith(".docx"):
        import docx
        document = docx.Document(io.BytesIO(uploaded_file.read()))
        return "\n".join(p.text for p in document.paragraphs)

    raise ValueError("Unsupported file type. Please upload a .txt, .pdf, or .docx file.")


def file_size_kb(uploaded_file):
    return round(len(uploaded_file.getvalue()) / 1024, 1)
