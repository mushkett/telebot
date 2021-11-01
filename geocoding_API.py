from configparser import ConfigParser
import requests
import json

config = ConfigParser()
config.read('config.ini')
GEOCODING_API_KEY = config.get('auth', 'GEOCODING_API_KEY')

def get_city_latitude(country, state, city):
    req = requests.get(f"https://graphhopper.com/api/1/geocode?q={city}&locale=en&debug=true&key={GEOCODING_API_KEY}") \
        .text
    json_dict = json.loads(req)

    for i in json_dict['hits']:
        if 'state' in i:
            if i['country'] == country and i['state'] == state and i['name'] == city:
                coord = {'lat': i['point']['lat'], 'lng': i['point']['lng']}
                return coord
