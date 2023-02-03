import requests


# получаем ответ от geocoder
def get_place_toponym(place: str) -> requests.Response:
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": place,
        "format": "json"
    }

    response = requests.get(geocoder_api_server, params=geocoder_params)
    return response


# получаем ответ от static maps
def get_place_map(data) -> requests.Response:
    map_params = {
        "ll": ",".join(list(map(str, data.coords))),
        'l': data.display,
        "spn": f"{data.spn},{data.spn}"
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    return response
