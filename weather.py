from datetime import datetime, timedelta
from configparser import ConfigParser
import requests
import json
import database


config = ConfigParser()
config.read('config.ini')
API_KEY = GEOCODING_API_KEY = config.get('auth', 'API_KEY')


def weather_1_day(chat_id):
    coord = database.get_location(chat_id)
    if type(coord) == str:
        return coord

    req = requests.get(f"https://api.openweathermap.org/data/2.5/onecall?lat={coord['lat']}&lon={coord['lng']}"
                       f"&exclude=hourly,current,minutely,alerts&appid={API_KEY}").text
    json_dict = json.loads(req)

    day = json_dict['daily'][0]

    summary_weather = f"{datetime.utcfromtimestamp(day['dt']).strftime('%d.%m.%Y')} \n" \
                      f"Temperature: {round(day['temp']['min']-273.15,1)} - {round(day['temp']['max']-273.15,1)} \n" \
                      f"Weather: {day['weather'][0]['description']} \n" \
                      f"Sunrise:" \
                      f" {(datetime.utcfromtimestamp(day['sunrise']) + timedelta(hours=2)).strftime('%H:%m')} \n" \
                      f"Sunset: " \
                      f"{(datetime.utcfromtimestamp(day['sunset']) + timedelta(hours=2)).strftime('%H:%m')}"

    return summary_weather

def weather_several_days(chat_id, days):
    coord = database.get_location(chat_id)
    if type(coord) == str:
        return coord

    req = requests.get(f"https://api.openweathermap.org/data/2.5/onecall?lat={coord['lat']}&lon={coord['lng']}"
                       f"&exclude=hourly,current,minutely,alerts&appid={API_KEY}").text
    json_dict = json.loads(req)

    summary_weather = ''
    for i in range(0, days):
        day = json_dict['daily'][i]
        summary_weather += f"{datetime.utcfromtimestamp(day['dt']).strftime('%d.%m.%Y')} \n" \
                           f"Temperature: {round(day['temp']['min'] - 273.15, 1)} - {round(day['temp']['max'] - 273.15, 1)} \n" \
                           f"Weather: {day['weather'][0]['description']} \n" \
                           f"\n"
    return summary_weather


