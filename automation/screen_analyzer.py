from PIL import Image
import pytesseract

from langchain_ollama import OllamaLLM

# =====================================================
# TESSERACT PATH
# =====================================================

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# =====================================================
# LOAD AI MODEL
# =====================================================

llm = OllamaLLM(
    model="phi3",
    temperature=0.1
)

# =====================================================
# EXTRACT TEXT FROM IMAGE
# =====================================================

def extract_text(image_path):

    try:

        image = Image.open(image_path)

        text = pytesseract.image_to_string(image)

        return text

    except Exception as e:

        return f"OCR Error: {e}"

# =====================================================
# ANALYZE SCREENSHOT
# =====================================================

def analyze_screenshot(image_path):

    text = extract_text(image_path)

    prompt = f"""
Analyze this screenshot text briefly.

Text:
{text[:700]}

Analysis:
"""

    try:

        print("\nJARVIS analyzing screenshot...\n")

        response = llm.invoke(
            prompt[:900]
        )

        return response[:250]

    except Exception as e:

        return f"AI Error: {e}"