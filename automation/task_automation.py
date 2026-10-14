"""Legacy desktop automation helpers.

This module is retained as a capability surface, not as an independent JARVIS
runtime. Importing it must never start a scheduler or an infinite loop.
Canonical mission authority remains GOVI -> JARVIS-NEXT; these helpers should
only be invoked by an approved worker task.
"""

import subprocess
import webbrowser


def morning_routine():
    """Open the legacy morning desktop routine."""
    webbrowser.open("https://news.google.com")
    webbrowser.open("https://mail.google.com")
    subprocess.Popen("notepad.exe")


def open_youtube():
    """Open YouTube as an explicit desktop capability."""
    webbrowser.open("https://www.youtube.com")


def research_mode():
    """Open the legacy research destinations."""
    webbrowser.open("https://pubmed.ncbi.nlm.nih.gov")
    webbrowser.open("https://scholar.google.com")


def run_scheduled_loop(schedule_module=None):
    """Run the optional legacy scheduler when explicitly invoked.

    The old module executed this loop at import time, creating a second
    autonomous runtime. Keeping the loop behind an explicit function preserves
    compatibility without allowing imports to start background execution.
    """
    if schedule_module is None:
        import schedule as schedule_module

    schedule_module.every().day.at("08:00").do(morning_routine)
    schedule_module.every().day.at("18:00").do(research_mode)

    while True:
        schedule_module.run_pending()
        import time
        time.sleep(1)


if __name__ == "__main__":
    run_scheduled_loop()
