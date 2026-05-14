import os
import subprocess
import webbrowser

# =====================================================
# OPEN COMMON APPS
# =====================================================

def open_chrome():

    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    if os.path.exists(chrome_path):

        subprocess.Popen(chrome_path)

def open_edge():

    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

    if os.path.exists(edge_path):

        subprocess.Popen(edge_path)

def open_notepad():

    subprocess.Popen("notepad.exe")

def open_calculator():

    subprocess.Popen("calc.exe")

def open_cmd():

    subprocess.Popen("cmd.exe")

def open_paint():

    subprocess.Popen("mspaint.exe")

# =====================================================
# OPEN FOLDERS
# =====================================================

def open_downloads():

    downloads = os.path.expanduser(
        "~/Downloads"
    )

    os.startfile(downloads)

def open_documents():

    documents = os.path.expanduser(
        "~/Documents"
    )

    os.startfile(documents)

def open_desktop():

    desktop = os.path.expanduser(
        "~/Desktop"
    )

    os.startfile(desktop)

# =====================================================
# WEB FUNCTIONS
# =====================================================

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

# =====================================================
# GOOGLE SEARCH
# =====================================================

def search_google(query):

    url = f"https://www.google.com/search?q={query}"

    webbrowser.open(url)

# =====================================================
# SYSTEM FUNCTIONS
# =====================================================

def shutdown_pc():

    os.system("shutdown /s /t 5")

def restart_pc():

    os.system("shutdown /r /t 5")

def lock_pc():

    os.system(
        "rundll32.exe user32.dll,LockWorkStation"
    )