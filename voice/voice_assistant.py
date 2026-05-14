import speech_recognition as sr
import asyncio
import edge_tts
import pygame
import time
import os

# -----------------------------
# INIT PYGAME AUDIO
# -----------------------------

pygame.mixer.init()

# -----------------------------
# SPEECH RECOGNIZER
# -----------------------------

recognizer = sr.Recognizer()

# -----------------------------
# SPEAK FUNCTION
# -----------------------------

async def speak(text):

    print(f"\nJARVIS: {text}")

    filename = "voice.mp3"

    communicate = edge_tts.Communicate(
        text,
        voice="en-US-GuyNeural"
    )

    await communicate.save(filename)

    pygame.mixer.music.load(filename)

    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():

        time.sleep(0.1)

    pygame.mixer.music.unload()

    os.remove(filename)

# -----------------------------
# LISTEN FUNCTION
# -----------------------------

def listen():

    with sr.Microphone() as source:

        print("\nListening...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=1
        )

        audio = recognizer.listen(
            source,
            phrase_time_limit=5
        )

    try:

        print("Recognizing...")

        command = recognizer.recognize_google(audio)

        print(f"\nYou said: {command}")

        return command.lower()

    except sr.UnknownValueError:

        print("Could not understand audio.")

        return ""

    except Exception as e:

        print("Error:", e)

        return ""

# -----------------------------
# STARTUP
# -----------------------------

asyncio.run(
    speak(
        "Hello Doctor Ramesh. JARVIS voice assistant is now online."
    )
)

# -----------------------------
# MAIN LOOP
# -----------------------------

while True:

    command = listen()

    if command == "":
        continue

    # EXIT
    if (
        "exit" in command
        or "shutdown" in command
        or "stop" in command
    ):

        asyncio.run(
            speak(
                "Shutting down. Goodbye Doctor."
            )
        )

        break

    # GREETING
    elif "hello" in command:

        asyncio.run(
            speak(
                "Hello Doctor. How can I assist you today?"
            )
        )

    # NAME
    elif "your name" in command:

        asyncio.run(
            speak(
                "I am JARVIS, your AI assistant."
            )
        )

    # STATUS
    elif "how are you" in command:

        asyncio.run(
            speak(
                "All systems are functioning perfectly Doctor."
            )
        )

    # DEFAULT
    else:

        asyncio.run(
            speak(
                f"You said {command}"
            )
        )