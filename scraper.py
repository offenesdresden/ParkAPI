__author__ = 'kilian'

import importlib
import requests
from datetime import datetime
import os
import json

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
    data["last_downloaded"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return data

def pipeline(city):
    """Take a city name and go through the process of parsing and processing the data"""
    data = add_metadata(parse_html(city, get_html(city)))
    save_data_to_disk(data, city.file_name)
    return data

def save_data_to_disk(data, city):
    """Save a data dictionary in ./cache as a json file"""
    if not os.path.exists("./cache"):
                os.mkdir("./cache")

    file = open("./cache/" + city + ".json", "w")
    file.write(json.dumps(data))
    file.close()

def live(city_name):
    """Scrape data for a given city pulling all data now"""
    try:
        city = importlib.import_module("cities." + city_name)
        return pipeline(city)
    except ImportError:
        # Couldn't find module for city
        return {"error": "Sorry, '" + city_name + "' isn't supported at the current time."}

def main():
    """Iterate over all cities in ./cities and scrape and save their data"""
    for file in os.listdir(os.curdir + "/cities"):
        if file.endswith(".py") and "__Init__" not in file.title() and "Sample_City" not in file.title():
            city = importlib.import_module("cities." + file.title()[:-3])
            data = pipeline(city)

            save_data_to_disk(data, file.title()[:-3])

if __name__ == "__main__":
    main()
