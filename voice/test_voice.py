import pyttsx3

engine = pyttsx3.init()

voices = engine.getProperty('voices')

print(voices)

engine.setProperty('rate', 170)

engine.say("Hello Doctor Ramesh. Voice system is working.")

engine.runAndWait()