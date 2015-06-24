import importlib
import requests
from datetime import datetime
import os
import json
import configparser
from bs4 import BeautifulSoup
import util
from security import file_is_allowed
import api_conf


USER_AGENT = "ParkAPI v{} - Info: {}".format(api_conf.VERSION, api_conf.SOURCE_REPOSITORY)


def get_html(city, server_mail=""):
    """Download html data for a given city"""
    headers = {
        "User-Agent": USER_AGENT,
        "From": server_mail
    }
    r = requests.get(city.data_url, headers=headers)

    # Requests fails to correctly check the encoding for every site,
    # we're going to have to get that manually (in some cases). This sucks.
    soup = BeautifulSoup(r.text)
    meta_content = soup.find("meta", {"http-equiv": "content-type"})
    if meta_content is not None:
        encoding = meta_content["content"].split("=")[-1]
        r.encoding = encoding

    return r.text


def parse_html(city, html):
    """Use a city module to parse it's html"""
    return city.parse_html(html)


def add_metadata(data):
    """Adds metadata to a scraped output dict"""
    data["last_downloaded"] = util.utc_now()
    return data


def pipeline(city, html):
    """Take a city name and html data and go through the process of parsing and processing the data"""
    data = add_metadata(parse_html(city, html))
    save_data_to_disk(data, city.file_name)
    return data


def save_data_to_disk(data, city):
    """Save a data dictionary in ./cache as a json file"""
    if not os.path.exists(api_conf.CACHE_DIRECTORY):
        os.mkdir(api_conf.CACHE_DIRECTORY)

    with open(os.path.join(api_conf.CACHE_DIRECTORY, city + ".json"), "w") as file:
        json.dump(data, fp=file)


def live(city_name, debug=False):
    """Scrape data for a given city pulling all data now"""
    try:
        city = importlib.import_module("cities." + city_name)
        if not debug:
            html = get_html(city)
            return pipeline(city, html)
        else:
            with open(os.path.join("tests", "fixtures", city_name + ".html")) as html:
                return pipeline(city, html)
    except ImportError:
        # Couldn't find module for city
        return {"error": "Sorry, '{}' isn't supported at the current time.".format(city_name)}


def main():
    """Iterate over all cities in ./cities, scrape and save their data"""

    try:
        config = configparser.ConfigParser()
        config.read("config.ini")
        server_mail = config["Server"]["mail"]
    except (KeyError, ValueError):
        server_mail = ""

    for file in filter(file_is_allowed, os.listdir(os.curdir + "/cities")):
        city = importlib.import_module("cities." + file.title()[:-3])

        html = get_html(city, server_mail=server_mail)
        data = pipeline(city, html)

        save_data_to_disk(data, file.title()[:-3])


if __name__ == "__main__":
    main()
