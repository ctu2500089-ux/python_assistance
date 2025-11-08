import sounddevice as sd
import numpy as np
import speech_recognition as sr
import pyttsx3
import os
import webbrowser

engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    print("AI:", text)
    engine.say(text)
    engine.runAndWait()


def listen(duration=5 , fs=16000):
    speak("Listening...")

    try:
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()

        audio_bytes = audio.tobytes()
        audio_data = sr.AudioData(audio_bytes, fs, 2)

        return audio_data

    except Exception as e:
        print("[MIC ERROR]:", e)
        speak("Microphone error.")
        return None


def get_text():
    recognizer = sr.Recognizer()
    audio_data = listen()

    if audio_data is None:
        return ""

    try:
        text = recognizer.recognize_google(audio_data)
        print("You said:", text)
        return text.lower()

    except Exception as e:
        print("[RECOGNITION ERROR]:", e)
        speak("I didn't understand.")
        return ""


# ✅ FIXED: Do NOT put webbrowser.open inside dictionary
def open_software(name):
    apps = {
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "browser": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "file explorer": "explorer.exe",
        "notepad": "notepad.exe",
    }

    if name in apps:
        os.startfile(apps[name])
        speak(f"Opening {name}")
    else:
        speak("Software not found.")


# ✅ Separate function for YouTube
def open_youtube():
    webbrowser.open("https://www.youtube.com")
    speak("Opening YouTube")

def play_music(song):
    url = f"https://www.youtube.com/results?search_query={song}+song"
    webbrowser.open(url)
    speak(f"Playing music: {song}")

def play_video(query):
    url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(url)
    speak(f"Playing video: {query}")


def create_file():
    with open("assistant_output.txt", "w") as f:
        f.write("This file is created by your assistant.")
    speak("File created.")


def assistant():
    speak("Voice assistant started.")

    while True:
        command = get_text()
        if command == "":
            continue

        if "open chrome" in command:
            open_software("chrome")

        elif "open browser" in command:
            open_software("browser")

        elif "open files" in command or "open file explorer" in command:
            open_software("file explorer")

        elif "open notepad" in command:
            open_software("notepad")

        elif "open youtube" in command:
            open_youtube()
        
        elif "play music" in command:
            song = command.replace("play music", "").strip()
            play_music(song)

        elif "play video" in command:
            query = command.replace("play video", "").strip()
            play_video(query)

        elif "create file" in command:
            create_file()

        elif "stop" in command or "exit" in command:
            speak("Goodbye!")
            break

assistant()

