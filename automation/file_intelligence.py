import os
from PIL import Image
import pytesseract
from docx import Document
from PyPDF2 import PdfReader

# =====================================================
# TESSERACT PATH
# =====================================================

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# =====================================================
# READ TEXT FILE
# =====================================================

def read_text_file(path):

    try:

        with open(path, "r", encoding="utf-8") as file:

            return file.read()

    except Exception as e:

        return f"Error reading file: {e}"

# =====================================================
# READ DOCX FILE
# =====================================================

def read_docx_file(path):

    try:

        doc = Document(path)

        full_text = []

        for para in doc.paragraphs:

            full_text.append(para.text)

        return "\n".join(full_text)

    except Exception as e:

        return f"Error reading DOCX: {e}"

# =====================================================
# READ PDF FILE
# =====================================================

def read_pdf_file(path):

    try:

        reader = PdfReader(path)

        text = ""

        for page in reader.pages:

            text += page.extract_text()

        return text

    except Exception as e:

        return f"Error reading PDF: {e}"

# =====================================================
# READ IMAGE TEXT (OCR)
# =====================================================

def read_image_text(path):

    try:

        image = Image.open(path)

        text = pytesseract.image_to_string(image)

        return text

    except Exception as e:

        return f"Error reading image: {e}"

# =====================================================
# SEARCH FILES
# =====================================================

def search_files(folder, keyword):

    matches = []

    for root, dirs, files in os.walk(folder):

        for file in files:

            if keyword.lower() in file.lower():

                matches.append(
                    os.path.join(root, file)
                )

    return matches