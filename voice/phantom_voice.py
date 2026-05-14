import os
import sys
import time
import tempfile

import sounddevice as sd
import scipy.io.wavfile as wav

import whisper

import pyttsx3

from langchain_ollama import OllamaLLM

# =====================================================
# FIX PATH
# =====================================================

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from memory.memory_manager import *

# =====================================================
# SETTINGS
# =====================================================

MODEL_NAME = "tinyllama"

SAMPLE_RATE = 16000

RECORD_SECONDS = 4

MAX_RESPONSE_CHARS = 180

# =====================================================
# LOAD WHISPER
# =====================================================

print("\nLoading Whisper model...\n")

whisper_model = whisper.load_model(
    "tiny"
)

print("Whisper loaded.\n")

# =====================================================
# LOAD AI
# =====================================================

print("Loading AI model...\n")

llm = OllamaLLM(
    model=MODEL_NAME
)

print("AI loaded.\n")

# =====================================================
# VOICE ENGINE
# =====================================================

engine = pyttsx3.init()

engine.setProperty(
    "rate",
    180
)

engine.setProperty(
    "volume",
    1.0
)

# =====================================================
# MEMORY
# =====================================================

conversation_history = []

# =====================================================
# SPEAK
# =====================================================

def speak(text):

    print(f"\nJARVIS: {text}\n")

    try:

        engine.stop()

        engine.say(text)

        engine.runAndWait()

    except:

        pass

# =====================================================
# RECORD AUDIO
# =====================================================

def record_audio():

    print("Listening...\n")

    audio = sd.rec(

        int(RECORD_SECONDS * SAMPLE_RATE),

        samplerate=SAMPLE_RATE,

        channels=1,

        dtype="int16"
    )

    sd.wait()

    temp_file = tempfile.NamedTemporaryFile(

        suffix=".wav",

        delete=False
    )

    wav.write(

        temp_file.name,

        SAMPLE_RATE,

        audio
    )

    return temp_file.name

# =====================================================
# TRANSCRIBE
# =====================================================

def transcribe_audio(file_path):

    try:

        print("Recognizing...\n")

        result = whisper_model.transcribe(

            file_path,

            fp16=False,

            language="en"
        )

        text = result["text"].strip().lower()

        if len(text) < 2:

            return ""

        garbage = [

            "thank you",

            "thanks for watching",

            "subtitle",

            "foreign",

            "music"
        ]

        for g in garbage:

            if g in text:

                return ""

        print(f"You said: {text}\n")

        return text

    except:

        return ""

# =====================================================
# MEMORY ENGINE
# =====================================================

def process_memory(command):

    memory = load_memory()

    # =================================================
    # STORE NAME
    # =================================================

    if "my name is" in command:

        value = command.split(
            "my name is",
            1
        )[1].strip()

        remember(
            "name",
            value
        )

        return (
            f"I remembered your name as "
            f"{value}"
        )

    # =================================================
    # RECALL NAME
    # =================================================

    if (
        "what is my name" in command
        or
        "what's my name" in command
    ):

        if "name" in memory:

            return (
                f"Your name is "
                f"{memory['name']}"
            )

        return (
            "I do not remember your name yet."
        )

    # =================================================
    # STORE COMPANY
    # =================================================

    if (
        "my company is" in command
        or
        "my company name is" in command
    ):

        if "my company name is" in command:

            value = command.split(
                "my company name is",
                1
            )[1].strip()

        else:

            value = command.split(
                "my company is",
                1
            )[1].strip()

        remember(
            "company",
            value
        )

        return (
            f"I remembered your company as "
            f"{value}"
        )

    # =================================================
    # RECALL COMPANY
    # =================================================

    if (
        "what is my company" in command
        or
        "what is my company name" in command
    ):

        if "company" in memory:

            return (
                f"Your company is "
                f"{memory['company']}"
            )

        return (
            "I do not remember your company yet."
        )

    return None

# =====================================================
# CLEAN RESPONSE
# =====================================================

def clean_response(text):

    text = text.replace(
        "\\n",
        " "
    )

    text = text.strip()

    # =============================================
    # LIMIT LENGTH
    # =============================================

    if len(text) > MAX_RESPONSE_CHARS:

        text = text[:MAX_RESPONSE_CHARS]

    # =============================================
    # CUT BAD ENDINGS
    # =============================================

    endings = [
        ".",
        "!",
        "?"
    ]

    for i in range(
        len(text) - 1,
        0,
        -1
    ):

        if text[i] in endings:

            text = text[:i + 1]

            break

    return text

# =====================================================
# AI RESPONSE
# =====================================================

def ask_ai(prompt):

    memory = load_memory()

    context = f"""

You are JARVIS.

You are a realtime voice assistant.

IMPORTANT RULES:

- Keep responses under 2 sentences
- Speak naturally
- Be concise
- Do not explain too much
- Respond like ChatGPT Voice
- Respond like Vapi AI
- Respond like Retell AI

Memory:
{memory}

User:
{prompt}

Assistant:
"""

    try:

        response = llm.invoke(

            context[:1200]

        )

        return clean_response(
            response
        )

    except Exception as e:

        print(f"AI Error: {e}")

        return (
            "I encountered an AI issue."
        )

# =====================================================
# PROCESS COMMAND
# =====================================================

def process_command(command):

    # =============================================
    # EXIT
    # =============================================

    if (
        "shutdown" in command
        or
        "exit" in command
        or
        "stop jarvis" in command
    ):

        speak("Shutting down.")

        sys.exit()

    # =============================================
    # MEMORY
    # =============================================

    memory_response = process_memory(
        command
    )

    if memory_response:

        speak(memory_response)

        return

    # =============================================
    # AI
    # =============================================

    print("Thinking...\n")

    response = ask_ai(command)

    speak(response)

# =====================================================
# MAIN LOOP
# =====================================================

def run_jarvis():

    speak(
        "PhantomOps conversational AI online."
    )

    while True:

        try:

            audio_file = record_audio()

            command = transcribe_audio(
                audio_file
            )

            if command == "":

                continue

            process_command(command)

        except KeyboardInterrupt:

            print("\nStopped.\n")

            break

        except Exception as e:

            print(f"System Error: {e}")

            time.sleep(1)

# =====================================================
# START
# =====================================================

run_jarvis()