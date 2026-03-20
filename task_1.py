import requests


URLS = [
    "https://github.com/",
    "https://www.binance.com/en",
    "https://tomtit.tomsk.ru/",
    "https://jsonplaceholder.typicode.com/",
    "https://moodle.tomtit-tomsk.ru/",
]


def get_status(code):
    if code == 200:
        return "доступен"
    if code == 403:
        return "вход запрещен"
    if code == 404:
        return "не найден"
    if code >= 500:
        return "не доступен"
    return "неизвестно"


for url in URLS:
    try:
        response = requests.get(url, timeout=5)
        status = get_status(response.status_code)
        print(f"{url} – {status} – {response.status_code}")
    except requests.RequestException:
        print(f"{url} – не доступен – ошибка")