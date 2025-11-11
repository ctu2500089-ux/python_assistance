import sounddevice as sd
import numpy as np
import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import datetime
import requests

engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    print("AI:", text)
    engine.say(text)
    engine.runAndWait()

def tell_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {now}")

def tell_date():
    today = datetime.datetime.now().strftime("%A, %d %B %Y")
    speak(f"Today is {today}")

def get_weather(city="Jagraon"):
    API_KEY = "37cb16168adb70d258f3093d3fa0bd08" 
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={API_KEY}&units=metric"
        )
        data = requests.get(url).json()
        # print("DEBUG weather data:", data)     

        if data.get("cod") != 200:
            message = data.get("message", "")
            speak(f"City not found: {city}. {message}")
            return

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        condition = data["weather"][0]["description"]

        speak(f"The weather in {city} is {condition} with temperature {temp}°C and humidity {humidity}%.")
    except Exception as e:
        speak("Unable to fetch weather.")
        print("[WEATHER ERROR]:", e)

def listen(duration=5, fs=16000):
    """Record audio using sounddevice and return as speech_recognition AudioData"""
    try:
        print("🎤 Listening...")
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        audio_bytes = audio.tobytes()
        return sr.AudioData(audio_bytes, fs, 2)
    except Exception as e:
        print("[MIC ERROR]:", e)
        speak("Microphone error.")
        return None

def get_text():
    recognizer = sr.Recognizer()
    audio_data = listen()

    if not audio_data:
        return ""

    try:
        text = recognizer.recognize_google(audio_data).lower().strip()
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        speak("I didn't understand.")
        return ""
    except sr.RequestError:
        speak("Sorry, Google service is not available.")
        return ""
    except Exception as e:
        speak("Something went wrong.")
        print("Error:", e)
        return ""

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

        if "time" in command:
            tell_time()
        elif "date" in command:
            tell_date()
        elif "weather" in command:
            if "in" in command:
                city = command.split("in")[-1].strip()
            else:
                city = "jagraon"
            get_weather(city)
        elif "open chrome" in command:
            open_software("chrome")
        elif "open browser" in command:
            open_software("browser")
        elif "open file" in command:
            open_software("file explorer")
        elif "open notepad" in command:
            open_software("notepad")
        elif "open youtube" in command or "youtube" in command:
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