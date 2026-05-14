import telebot
import webbrowser
import subprocess
import os

from langchain_ollama import OllamaLLM

# =====================================================
# BOT TOKEN
# =====================================================

BOT_TOKEN = "8246686795:AAGxU533CPCrleLOcyaDmFSE3g_AJjttnSE"

# =====================================================
# YOUR TELEGRAM CHAT ID
# =====================================================

AUTHORIZED_CHAT_ID = 7238244143s
# =====================================================
# CREATE TELEGRAM BOT
# =====================================================

bot = telebot.TeleBot(BOT_TOKEN)

# =====================================================
# LOAD AI MODEL
# =====================================================

llm = OllamaLLM(
    model="phi3",
    temperature=0.2
)

# =====================================================
# SECURITY CHECK
# =====================================================

def authorized(message):

    return message.chat.id == AUTHORIZED_CHAT_ID

# =====================================================
# WEBSITE FUNCTIONS
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
# SEARCH GOOGLE
# =====================================================

def search_google(query):

    url = f"https://www.google.com/search?q={query}"

    webbrowser.open(url)

# =====================================================
# OPEN APPLICATIONS
# =====================================================

def open_calculator():

    subprocess.Popen("calc.exe")

def open_notepad():

    subprocess.Popen("notepad.exe")

def open_cmd():

    subprocess.Popen("cmd.exe")

# =====================================================
# START COMMAND
# =====================================================

@bot.message_handler(commands=['start'])

def start(message):

    if not authorized(message):

        return

    print("Authorized user connected.")

    bot.reply_to(
        message,
        "🤖 JARVIS Telegram Control Online."
    )

# =====================================================
# MAIN MESSAGE HANDLER
# =====================================================

@bot.message_handler(func=lambda message: True)

def handle_message(message):

    if not authorized(message):

        return

    command = message.text.lower()

    print(f"\nTelegram Command: {command}")

    # =================================================
    # OPEN YOUTUBE
    # =================================================

    if "open youtube" in command:

        open_youtube()

        bot.reply_to(
            message,
            "Opening YouTube."
        )

    # =================================================
    # OPEN GOOGLE
    # =================================================

    elif "open google" in command:

        open_google()

        bot.reply_to(
            message,
            "Opening Google."
        )

    # =================================================
    # OPEN CHATGPT
    # =================================================

    elif "open chatgpt" in command:

        open_chatgpt()

        bot.reply_to(
            message,
            "Opening ChatGPT."
        )

    # =================================================
    # OPEN CALCULATOR
    # =================================================

    elif "open calculator" in command:

        open_calculator()

        bot.reply_to(
            message,
            "Opening calculator."
        )

    # =================================================
    # OPEN NOTEPAD
    # =================================================

    elif "open notepad" in command:

        open_notepad()

        bot.reply_to(
            message,
            "Opening notepad."
        )

    # =================================================
    # OPEN COMMAND PROMPT
    # =================================================

    elif "open command prompt" in command:

        open_cmd()

        bot.reply_to(
            message,
            "Opening command prompt."
        )

    # =================================================
    # GOOGLE SEARCH
    # =================================================

    elif "search google for" in command:

        search = command.replace(
            "search google for",
            ""
        )

        search_google(search)

        bot.reply_to(
            message,
            f"Searching Google for: {search}"
        )

    # =================================================
    # AI RESPONSE
    # =================================================

    else:

        try:

            prompt = f"""
You are JARVIS.

Rules:
- Your name is JARVIS.
- Never say you are Phi.
- Never mention Microsoft.
- Answer briefly and intelligently.

User:
{command}

JARVIS:
"""

            response = llm.invoke(
                prompt[:300]
            )

            response = response[:500]

            bot.reply_to(
                message,
                response
            )

        except Exception as e:

            print("AI Error:", e)

            bot.reply_to(
                message,
                "AI processing error."
            )

# =====================================================
# START BOT
# =====================================================

print("🤖 TELEGRAM JARVIS RUNNING...")

while True:

    try:

        print("🤖 TELEGRAM JARVIS RUNNING...")

        bot.infinity_polling(
            timeout=30,
            long_polling_timeout=30
        )

    except Exception as e:

        print(f"Telegram Error: {e}")