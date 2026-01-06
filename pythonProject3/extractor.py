# extractor.py
import pdfplumber

def extract_text_from_pdf(file_like):
    """Extract text from an uploaded PDF (file_like is a BytesIO / UploadedFile).
    Returns a single string.
    """
    text = []
    with pdfplumber.open(file_like) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
    return "\n".join(text)