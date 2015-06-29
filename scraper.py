import importlib
import requests
import os
import json
import configparser
from bs4 import BeautifulSoup
import psycopg2
import util
from security import file_is_allowed
import api_conf

USER_AGENT = "ParkAPI v{} - Info: {}".format(api_conf.SERVER_VERSION, api_conf.SOURCE_REPOSITORY)


def get_html(city):
    """Download html data for a given city"""
    headers = {
        "User-Agent": USER_AGENT
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
    """Use a city module to parse its html"""
    return city.parse_html(html)


def add_metadata(data):
    """Adds metadata to a scraped output dict"""
    data["last_downloaded"] = util.utc_now()
    return data


# def save_data_to_disk(data, city):
#     """Save a data dictionary in ./cache as a json file"""
#     if not os.path.exists(api_conf.CACHE_DIRECTORY):
#         os.mkdir(api_conf.CACHE_DIRECTORY)
#
#     with open(os.path.join(api_conf.CACHE_DIRECTORY, os.path.basename(city.__file__) + ".json"), "w") as file:
#         json.dump(data, fp=file)


def connect_to_db(db_data):
    """Return a connection to the Postgres database"""
    return psycopg2.connect(database=db_data["name"], user=db_data["user"], host=db_data["host"],
                            port=db_data["port"], password=db_data["pass"])


def save_data_to_db(cursor, parking_data, city):
    """Save the data given into the Postgres DB."""
    timestamp_updated = parking_data["last_updated"]
    timestamp_downloaded = util.utc_now()
    json_data = json.dumps(parking_data)
    sql_string = "INSERT INTO parkapi(timestamp_updated, timestamp_downloaded, city, data) " \
                 "VALUES (%(updated)s, %(downloaded)s, %(city)s, %(data)s) RETURNING 'id';"
    cursor.execute(sql_string, {
        "updated": timestamp_updated,
        "downloaded": timestamp_downloaded,
        "city": city,
        "data": json_data
    })

    print("Saved " + city + " to DB.")


def _live(city_name):
    """
    Scrape data for a given city pulling all data now
    This function is only used in development mode for debugging the server without a database present.
    """
    try:
        city = importlib.import_module("cities." + city_name)
        data = add_metadata(parse_html(city, get_html(city)))
        return data
    except ImportError:
        # Couldn't find module for city
        return {"error": "Sorry, '{}' isn't supported at the current time.".format(city_name)}


def main():
    """Iterate over all cities in ./cities, scrape and save their data to the database"""

    config = configparser.ConfigParser()
    config.read("config.ini")

    db_data = {
        "host": config["Database"]["host"],
        "name": config["Database"]["name"],
        "user": config["Database"]["user"],
        "pass": config["Database"]["pass"],
        "port": config["Database"]["port"]
    }

    if db_data is not None:
        conn = connect_to_db(db_data)
        cursor = conn.cursor()

    for file in filter(file_is_allowed, os.listdir(os.curdir + "/cities")):
        city = importlib.import_module("cities." + file.title()[:-3])
        data = add_metadata(parse_html(city, get_html(city)))

        if cursor is not None:
            save_data_to_db(cursor, data, file.title()[:-3])

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
