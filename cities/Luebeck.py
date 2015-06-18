__author__ = 'kilian'

import requests
from bs4 import BeautifulSoup
import datetime

data_url = "http://kwlpls.adiwidjaja.info"
city_name = "Lübeck"
file_name = "Luebeck"

def parse_html(html):
    soup = BeautifulSoup(html)
    data = {
        "lots": []
    }

    # Letzte Aktualisierung auslesen
    date_last_changed = datetime.datetime.strptime(soup.find("tr").find("strong").text, "Stand: %d.%m.%Y, %H:%M Uhr")
    data["last_changed"] = str(date_last_changed)
    return data
