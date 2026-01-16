# import pdfplumber
#
# def extract_text_from_pdf(file_like):
#     text = []
#     with pdfplumber.open(file_like) as pdf:
#         for page in pdf.pages:
#             page_text = page.extract_text()
#             if page_text:
#                 text.append(page_text)
#     return "\n".join(text)


# import pdfplumber
# from PIL import Image
# import pytesseract
# import io
import pdfplumber
from PIL import Image
import pytesseract
import io

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ---------------------------
# OPTIONAL (Windows users only)
# If OCR fails, uncomment and set your Tesseract path:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# ---------------------------

def extract_text_from_pdf(file_like):
    text = []
    with pdfplumber.open(file_like) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
    return "\n".join(text)


def extract_text_from_image(file_like):
    image_bytes = file_like.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    text = pytesseract.image_to_string(image)
    return text


# ✅ THIS FUNCTION WAS MISSING
def extract_text(uploaded_file):
    """
    Detect file type automatically and extract text.
    Supports PDF, PNG, JPG, JPEG, WEBP
    """
    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)

    elif filename.endswith((".png", ".jpg", ".jpeg", ".webp")):
        return extract_text_from_image(uploaded_file)

    else:
        return ""
