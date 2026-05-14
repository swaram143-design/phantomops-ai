import schedule
import time
import webbrowser
import subprocess

# =====================================================
# TASK FUNCTIONS
# =====================================================

def morning_routine():

    print("Running morning routine...")

    webbrowser.open(
        "https://news.google.com"
    )

    webbrowser.open(
        "https://mail.google.com"
    )

    subprocess.Popen("notepad.exe")

def open_youtube():

    print("Opening YouTube...")

    webbrowser.open(
        "https://www.youtube.com"
    )

def research_mode():

    print("Starting research mode...")

    webbrowser.open(
        "https://pubmed.ncbi.nlm.nih.gov"
    )

    webbrowser.open(
        "https://scholar.google.com"
    )

# =====================================================
# SCHEDULE TASKS
# =====================================================

schedule.every().day.at("08:00").do(
    morning_routine
)

schedule.every().day.at("18:00").do(
    research_mode
)

# =====================================================
# MAIN LOOP
# =====================================================

print("🤖 JARVIS Automation Engine Running...")

while True:

    schedule.run_pending()

    time.sleep(1)