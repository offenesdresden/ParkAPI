__author__ = 'kilian'

import importlib
import requests
from datetime import datetime
import os

def get_html(city):
    """Download html data for a given city"""
    headers = {
        "User-Agent": "ParkAPI v0.1 - Info: https://github.com/kiliankoe/ParkAPI"
    }
    return requests.get(city.data_url, headers=headers).text

def parse_html(city, html):
    """Use a city module to parse it's html"""
    return city.parse_html(html)

def add_metadata(data):
    """Adds metadata to a scraped output dict"""
    data["time_scraped"] = datetime.now()
    return data

def live(city_name):
    # try to import the python file for the city
    try:
        city = importlib.import_module("cities." + city_name)
        html = get_html(city)
        data = parse_html(city, html)
        print(add_metadata(data))
        return add_metadata(data)

    except ImportError:
        # Couldn't find module for city
        return {"error": "Sorry, '" + city_name + "' isn't supported at the current time."}

def main():
    for file in os.listdir(os.curdir + "/cities"):
        if file.endswith(".py") and file is not "__init__.py" and file is not "Sample_City.py":
            print(file)

if __name__ == "__main__":
    live("Luebeck")
