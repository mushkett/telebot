import requests
import json
from datetime import datetime, timezone

API_KEY = "a210ef53e8cfbac54bf57636f90aa41e"


def print_weather(city_name):
    req = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&lang={lang}").text
    json_dict = json.loads(req)

    weather = json_dict['weather'][0]['description'].capitalize()
    temperature = round(json_dict['main']['temp'] - 273.15)
    feels_like = round(json_dict['main']['feels_like'] - 273.15)

    sunrise = datetime.utcfromtimestamp(json_dict['sys']['sunrise'])
    sunrise = sunrise.replace(sunrise.year, sunrise.month, sunrise.day, sunrise.hour+3).strftime(' %H:%M:%S')

    sunset = datetime.utcfromtimestamp(json_dict['sys']['sunset'])
    sunset = sunset.replace(sunset.year, sunset.month, sunset.day, sunset.hour+3).strftime(' %H:%M:%S')

    location = f"{json_dict['sys']['country']}, {json_dict['name']}"

    summary_weather = f"{location}\n" \
                      f"{weather}\n" \
                      f"Температура: {temperature} °C\n" \
                      f"Ощущается как: {feels_like} °C\n" \
                      f"Рассвет: {sunrise}\n" \
                      f"Закат: {sunset}"

    return summary_weather




def input_city():
    return input("Введите название города: ")


lang = 'ru'

