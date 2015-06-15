__author__ = 'kilian'

import requests
from bs4 import BeautifulSoup
import datetime

dataURL = "http://www.ingolstadt.mobi/parkplatzauskunft.cfm"

def _get_html():
    headers = {
        "User-Agent": "ParkAPI v0.1 - Info: https://github.com/kiliankoe/ParkAPI"
    }

    r = requests.get(dataURL, headers=headers)
    return r.text

def _parse_html():
    soup = BeautifulSoup(_get_html())

    # get time last updated
    data = {
        "last_updated": datetime.datetime.strptime(soup.p.string, "(%d.%m.%Y, %H.%M Uhr)"),
        "lots": []
    }

    # get all lots
    raw_lots = soup.find_all("tr")

    for lot in raw_lots:
        elements = lot.find_all("td")

        data["lots"].append({
            "name": elements[0].text,
            "free": int(elements[1].text)
        })

    return data

def get_data():
    return _parse_html()
