from langchain_ollama import OllamaLLM

from automation.file_intelligence import (
    read_text_file,
    read_docx_file,
    read_pdf_file
)

# =====================================================
# LOAD MODEL
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
# SHORT AI SUMMARY
# =====================================================

def summarize_text(text):

    # LIMIT INPUT
    text = clean_text(text[:600])

    prompt = f"""
Summarize this text in 2 short sentences only.

Text:
{text}

Summary:
"""

    try:

        print("\nJARVIS is analyzing...\n")

        response = llm.invoke(
            prompt[:800]
        )

        # HARD LIMIT OUTPUT
        response = response[:180]

        # CLEAN EXTRA GENERATION
        if "---" in response:

            response = response.split("---")[0]

        if "Instruction" in response:

            response = response.split("Instruction")[0]

        return response.strip()

    except Exception as e:

        return f"AI Error: {e}"

# =====================================================
# SUMMARIZE FILE
# =====================================================

def summarize_file(path):

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

    return summarize_text(text)