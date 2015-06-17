__author__ = 'kilian'

import requests
from bs4 import BeautifulSoup
import datetime

base_url = "http://kwlpls.adiwidjaja.info"

def _get_html():
    headers = {
        "User-Agent": "ParkAPI v0.1 - Info: https://github.com/kiliankoe/ParkAPI"
    }

    r = requests.get(base_url, headers=headers)
    return r.text

def _parse_html():
    soup = BeautifulSoup(_get_html())
    data = {
        "lots": []
    }

    # Letzte Aktualisierung auslesen
    date_last_changed = datetime.datetime.strptime(soup.find("tr").find("strong").text, "Stand: %d.%m.%Y, %H:%M Uhr")
    data["last_changed"] = date_last_changed
    return data


def get_data():
    return _parse_html()
