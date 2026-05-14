from langchain_ollama import OllamaLLM

from automation.file_intelligence import (
    read_text_file,
    read_docx_file,
    read_pdf_file
)

# =====================================================
# LOAD AI MODEL
# =====================================================

llm = OllamaLLM(
    model="phi3",
    temperature=0.1
)

# =====================================================
# CLEAN TEXT
# =====================================================

def clean_text(text):

    text = text.replace("\n", " ")

    text = text.replace("\r", " ")

    return text.strip()

# =====================================================
# ANALYZE MEDICAL REPORT
# =====================================================

def analyze_medical_report(text):

    text = clean_text(text[:1200])

    prompt = f"""
You are a medical AI assistant.

Analyze this medical report briefly.

Tasks:
- Summarize findings
- Mention important values
- Mention possible abnormalities
- Explain in simple language

Medical Report:
{text}

Analysis:
"""

    try:

        print("\nJARVIS analyzing medical report...\n")

        response = llm.invoke(
            prompt[:1500]
        )

        response = response[:700]

        return response.strip()

    except Exception as e:

        return f"AI Error: {e}"

# =====================================================
# READ FILE
# =====================================================

def analyze_file(path):

    # TXT
    if path.endswith(".txt"):

        text = read_text_file(path)

    # DOCX
    elif path.endswith(".docx"):

        text = read_docx_file(path)

    # PDF
    elif path.endswith(".pdf"):

        text = read_pdf_file(path)

    else:

        return "Unsupported file format."

    return analyze_medical_report(text)