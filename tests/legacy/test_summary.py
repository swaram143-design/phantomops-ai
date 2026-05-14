from automation.document_summarizer import *

result = summarize_file(
    "sample.txt"
)

print("\n===== SUMMARY =====\n")

print(result)