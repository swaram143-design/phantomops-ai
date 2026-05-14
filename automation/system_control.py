import webbrowser
import subprocess
import os

# -----------------------------
# OPEN WEBSITES
# -----------------------------

def open_youtube():

    webbrowser.open(
        "https://www.youtube.com"
    )

def open_google():

    webbrowser.open(
        "https://www.google.com"
    )

def open_chatgpt():

    webbrowser.open(
        "https://chat.openai.com"
    )

# -----------------------------
# GOOGLE SEARCH
# -----------------------------

def search_google(query):

    url = f"https://www.google.com/search?q={query}"

    webbrowser.open(url)

# -----------------------------
# OPEN APPLICATIONS
# -----------------------------

def open_calculator():

    subprocess.Popen("calc.exe")

def open_notepad():

    subprocess.Popen("notepad.exe")

def open_cmd():

    subprocess.Popen("cmd.exe")

# -----------------------------
# SYSTEM CONTROL
# -----------------------------

def shutdown_pc():

    os.system("shutdown /s /t 5")

def restart_pc():

    os.system("shutdown /r /t 5")