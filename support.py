import os

from dotenv import load_dotenv

import requests

# получаем ключ геокодера
load_dotenv()
GEOCODER_APIKEY = os.environ.get('GEOCODER_APIKEY', default='default')


# получаем ответ от geocoder
def get_place_toponym(
    place_name: str = None, coords: str = None
) -> requests.Response:
    geocoder_api_server = 'http://geocode-maps.yandex.ru/1.x/'

    geocoder_params = {
        'apikey': GEOCODER_APIKEY,
        'format': 'json',
    }
    if place_name:
        geocoder_params['geocode'] = place_name
    else:
        geocoder_params['geocode'] = coords

    response = requests.get(geocoder_api_server, params=geocoder_params)
    return response


# получаем ответ от static maps
def get_place_map(data) -> requests.Response:
    map_params = {
        'll': ','.join(list(map(str, data.coords))),
        'l': data.display,
        'spn': f'{data.spn},{data.spn}',
        'pt': data.pt,
    }

    map_api_server = 'http://static-maps.yandex.ru/1.x/'
    response = requests.get(map_api_server, params=map_params)
    return response
