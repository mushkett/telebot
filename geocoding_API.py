from configparser import ConfigParser
import requests
import json

config = ConfigParser()
config.read('config.ini')
GEOCODING_API_KEY = config.get('auth', 'GEOCODING_API_KEY')


def get_city_latitude(country, city):
    req = requests.get(f"https://graphhopper.com/api/1/geocode?q={city}&locale=en&debug=true&key={GEOCODING_API_KEY}") \
        .text
    json_dict = json.loads(req)

    for i in json_dict['hits']:
        if 'country' in i:
            if i['country'] == country and i['name'] == city:
                coord = {'lat': i['point']['lat'], 'lng': i['point']['lng']}
                return coord


def get_city_list(city):
    req = requests.get(f"https://graphhopper.com/api/1/geocode?q={city}&locale=en&debug=true&key={GEOCODING_API_KEY}") \
        .text
    json_dict = json.loads(req)
    n = 1
    location_options = {}
    for i in json_dict['hits']:
        if 'country' in i:
            if i['country'] not in location_options.values():
                location_options[n] = f'{i["country"]}'
                n += 1

    return location_options
