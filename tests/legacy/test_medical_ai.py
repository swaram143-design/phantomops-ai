from automation.medical_report_analyzer import *

result = analyze_file(
    "medical_report.txt"
)

print("\n===== MEDICAL ANALYSIS =====\n")

print(result)