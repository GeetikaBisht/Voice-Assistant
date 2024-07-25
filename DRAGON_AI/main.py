import pyttsx3
import speech_recognition as sr
import keyboard
import os
import subprocess as sp
import imdb
import pyautogui
import pyjokes
import wolframalpha
from datetime import datetime
from decouple import config
from random import choice
from conv import random_text
from online import find_my_ip, search_on_google, search_on_wikipedia, youtube, get_news, weather_forecast

engine = pyttsx3.init('sapi5')
engine.setProperty('volume', 1.0)
engine.setProperty('rate', 220)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

USER = config('USER', default='Geetika')
HOSTNAME = config('BOT', default='Dragon')


def speak(text):
    engine.say(text)
    engine.runAndWait()


def greet_me():
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good morning {USER}")
    elif (hour >= 12) and (hour <= 16):
        speak(f"Good afternoon {USER}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good evening {USER}")
    speak(f"I am {HOSTNAME}, your personal assistant. How may I assist you, {USER}?")


def start_listening():
    global listening
    listening = True
    print("Started listening")


def pause_listening():
    global listening
    listening = False
    print("Stopped listening")


keyboard.add_hotkey('ctrl+alt+g', start_listening)
keyboard.add_hotkey('ctrl+alt+e', pause_listening)


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(query)
        if 'stop' not in query and 'exit' not in query:
            speak(choice(random_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 or hour < 6:
                speak("Good night, take care!")
            else:
                speak("Have a good day!")
            exit()
    except Exception:
        speak("Sorry I couldn't understand. Can you please repeat that?")
        query = 'None'
    return query


if __name__ == '__main__':
    greet_me()
    while True:
        query = take_command().lower()
        if "how are you" in query:
            speak("I am absolutely fine. What about you")

        elif "open command prompt" in query:
            speak("Opening command prompt")
            os.system('start cmd')

        elif "open camera" in query:
            speak("Opening camera ")
            sp.run('start microsoft.windows.camera:', shell=True)

        elif "open notepad" in query:
            speak("Opening Notepad for you")
            notepad_path = "C:\\Windows\\notepad.exe"
            os.startfile(notepad_path)

        elif "open word" in query:
            speak("Opening Word for you")
            word_path = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Word"
            os.startfile(word_path)

        elif "open excel" in query:
            speak("Opening Excel for you")
            excel_path = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Excel"
            os.startfile(excel_path)

        elif "open powerpoint" in query:
            speak("Opening PowerPoint for you")
            powerpoint_path = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\PowerPoint"
            os.startfile(powerpoint_path)

        elif "open whatsapp" in query:
            speak("Opening WhatsApp for you")
            whatsapp_path = "https://web.whatsapp.com/"
            os.startfile(whatsapp_path)

        elif "take screenshot" in query:
            speak("Taking a screenshot")
            screenshot = pyautogui.screenshot()
            screenshot.save("screenshot.png")
            speak("Screenshot saved")

        elif "ip address" in query:
            ip_address = find_my_ip()
            speak(f"Your IP Address is {ip_address}")
            print(f"Your IP Address is {ip_address}")

        elif "open youtube" in query:
            speak("What do you want to play on YouTube?")
            video = take_command().lower()
            youtube(video)

        elif "open google" in query:
            speak(f"What do you want to search on Google {USER}?")
            query = take_command().lower()
            search_on_google(query)

        elif 'tell me a joke' in query:
            joke = pyjokes.get_joke()
            speak(joke)
            print(joke)

        elif 'time' in query:
            strTime = datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
            print(f"The time is {strTime}")

        elif "wikipedia" in query:
            speak("What do you want to search on Wikipedia?")
            search = take_command().lower()
            results = search_on_wikipedia(search)
            speak(f"According to Wikipedia, {results}")
            speak("I am printing it on the terminal")
            print(results)

        elif "give me news" in query:
            speak("I am reading out the latest headline of today")
            speak(get_news())
            speak("I am printing it on screen")
            print(*get_news(), sep='\n')

        elif 'weather' in query:
            ip_address = find_my_ip()
            speak("Tell me the name of your city")
            city = input("Enter name of your city: ")
            speak(f"Getting weather report for your city {city}")
            weather, temp, feels_like = weather_forecast(city)
            speak(f"The current temperature is {temp}, but it feels like {feels_like}")
            speak(f"Also, the weather report talks about {weather}")
            speak("For your convenience, I am printing it on the screen.")
            print(f"Description: {weather}\nTemperature: {temp}\nFeels like: {feels_like}")

        elif "movie" in query:
            movies_db = imdb.IMDb()
            speak("Please tell me the movie name:")
            text = take_command()
            movies = movies_db.search_movie(text)
            speak("Searching for " + text)
            speak("I found these")
            for movie in movies:
                title = movie["title"]
                year = movie["year"]
                speak(f"{title} - {year}")
                info = movie.getID()
                movie_info = movies_db.get_movie(info)
                rating = movie_info["rating"]
                cast = movie_info["cast"]
                actor = cast[0:5]
                plot = movie_info.get('plot outline', 'plot summary not available')
                speak(
                    f"{title} was released in {year} and has IMDb ratings of {rating}. It has a cast of {actor}. The plot summary of the movie is {plot}")

        elif "calculate" in query:
            app_id = "X6J9XK-VAAG9TQGYA"
            client = wolframalpha.Client(app_id)
            ind = query.lower().split().index("calculate")
            text = query.split()[ind + 1:]
            result = client.query(" ".join(text))
            try:
                ans = next(result.results).text
                speak("The answer is " + ans)
                print("The answer is " + ans)
            except StopIteration:
                speak("I couldn't find that. Please try again")

        elif 'what is' in query or 'who is' in query or 'which is' in query:
            app_id = "X6J9XK-VAAG9TQGYA"
            client = wolframalpha.Client(app_id)
            try:
                ind = query.lower().index('what is') if 'what is' in query.lower() else \
                    query.lower().index('who is') if 'who is' in query.lower() else \
                        query.lower().index('which is') if 'which is' in query.lower() else None

                if ind is not None:
                    text = query.split()[ind + 2:]
                    res = client.query(" ".join(text))
                    ans = next(res.results).text
                    speak("The answer is " + ans)
                    print("The answer is " + ans)
                else:
                    speak("I couldn't find that. Please try again.")
            except StopIteration:
                speak("I couldn't find that. Please try again.")


