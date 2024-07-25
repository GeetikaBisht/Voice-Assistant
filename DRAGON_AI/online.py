import requests
import wikipedia
import pywhatkit as kit
from decouple import config


def find_my_ip():
    ip_address = requests.get('https://api.ipify.org?format=json').json()
    return ip_address["ip"]


def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results


def search_on_google(query):
    kit.search(query)


def youtube(video):
    kit.playonyt(video)


def get_news():
    news_headline = []
    result = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&category=general&apiKey"f"=d32498f3cea246b89b8fda792343998b"
                        ).json()
    articles = result["articles"]
    for article in articles:
        news_headline.append(article["title"])
    return news_headline[:6]


def weather_forecast(city):
    res = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=2e5ac40a0b64c2f734c13308486981cc"
    ).json()
    weather = res["weather"][0]["main"]
    temp = res["main"]["temp"] - 273.15
    feels_like = res["main"]["feels_like"] - 273.15
    return weather, f"{temp:.2f}°C", f"{feels_like:.2f}°C"


