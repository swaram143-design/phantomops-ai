import os
import sys
import difflib

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

# =====================================================
# IMPORTS
# =====================================================

import speech_recognition as sr
import pyttsx3

from langchain_ollama import OllamaLLM

from memory.memory_manager import *

# =====================================================
# AI MODEL
# =====================================================

llm = OllamaLLM(
    model="llama3"
)

# =====================================================
# SPEECH ENGINE
# =====================================================

engine = pyttsx3.init()

engine.setProperty(
    "rate",
    155
)

# =====================================================
# RECOGNIZER
# =====================================================

recognizer = sr.Recognizer()

recognizer.pause_threshold = 1.5

recognizer.energy_threshold = 300

# =====================================================
# CONVERSATION MEMORY
# =====================================================

conversation_history = []

# =====================================================
# SPEAK
# =====================================================

def speak(text):

    print(f"\nJARVIS: {text}")

    engine.say(text)

    engine.runAndWait()

# =====================================================
# LISTEN
# =====================================================

def listen():

    try:

        with sr.Microphone() as source:

            print("\nListening...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            audio = recognizer.listen(

                source,

                timeout=20,

                phrase_time_limit=20
            )

            print("Recognizing...")

            command = recognizer.recognize_google(
                audio
            )

            command = command.lower().strip()

            print(f"\nYou said: {command}")

            return command

    except sr.WaitTimeoutError:

        print("Still waiting for speech...")

        return ""

    except sr.UnknownValueError:

        print("Could not understand audio.")

        return ""

    except Exception as e:

        print(f"Voice Error: {e}")

        return ""

# =====================================================
# FUZZY MATCH
# =====================================================

def similar(a, b):

    return difflib.SequenceMatcher(
        None,
        a,
        b
    ).ratio()

# =====================================================
# MEMORY ENGINE
# =====================================================

def process_memory(command):

    memory = load_memory()

    # =============================================
    # SHOW MEMORY
    # =============================================

    if (
        "what do you remember" in command
        or
        "do you remember" in command
    ):

        return str(memory)

    # =============================================
    # NAME MEMORY
    # =============================================

    if (
        "my name is" in command
        or
        "remember my name" in command
    ):

        if "is" in command:

            value = command.split(
                "is",
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

        return (
            "What should I remember "
            "your name as?"
        )

    # =============================================
    # COMPANY MEMORY
    # =============================================

    company_patterns = [

        "my company is",

        "my company name is",

        "remember my company as",

        "remember my company name as"
    ]

    for pattern in company_patterns:

        if pattern in command:

            value = command.split(
                pattern,
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

    # =============================================
    # PROJECT MEMORY
    # =============================================

    if "my project is" in command:

        value = command.split(
            "my project is",
            1
        )[1].strip()

        remember(
            "project",
            value
        )

        return (
            f"I remembered your project as "
            f"{value}"
        )

    # =============================================
    # WHAT IS MY
    # =============================================

    question_patterns = [

        "what is my",

        "what's my",

        "tell me my"
    ]

    for pattern in question_patterns:

        if pattern in command:

            key = command.replace(
                pattern,
                ""
            ).strip()

            # =====================================
            # NORMALIZATION
            # =====================================

            if "name" in key:

                key = "name"

            elif "company" in key:

                key = "company"

            elif "project" in key:

                key = "project"

            elif "goal" in key:

                key = "goal"

            # =====================================
            # DIRECT MATCH
            # =====================================

            if key in memory:

                return (
                    f"Your {key} is "
                    f"{memory[key]}"
                )

            # =====================================
            # FUZZY SEARCH
            # =====================================

            best_match = None

            best_score = 0

            for mem_key in memory.keys():

                score = similar(
                    key,
                    mem_key
                )

                if score > best_score:

                    best_score = score

                    best_match = mem_key

            if best_score > 0.45:

                return (
                    f"Your {best_match} is "
                    f"{memory[best_match]}"
                )

            return (
                "I do not remember that yet."
            )

    return None

# =====================================================
# AI RESPONSE
# =====================================================

def ask_ai(prompt):

    global conversation_history

    try:

        memory = load_memory()

        context = f"""

You are JARVIS, a highly intelligent conversational AI assistant.

User Memory:
{memory}

Recent Conversation:
{conversation_history[-5:]}

User Message:
{prompt}

Respond naturally like Siri or ChatGPT.

"""

        response = llm.invoke(context)

        conversation_history.append(
            {
                "user": prompt,
                "assistant": response
            }
        )

        return response

    except Exception as e:

        return f"AI Error: {e}"

# =====================================================
# MAIN LOOP
# =====================================================

def run_jarvis():

    speak(
        "Jarvis conversational AI online."
    )

    while True:

        command = listen()

        if command == "":

            continue

        # =============================================
        # EXIT
        # =============================================

        if (
            "exit" in command
            or
            "shutdown" in command
        ):

            speak("Shutting down.")

            break

        # =============================================
        # MEMORY SYSTEM
        # =============================================

        memory_response = process_memory(
            command
        )

        if memory_response:

            speak(memory_response)

            continue

        # =============================================
        # AI SYSTEM
        # =============================================

        print("\nThinking...\n")

        response = ask_ai(command)

        speak(response)

# =====================================================
# START
# =====================================================

run_jarvis()