#!/usr/bin/env python
import json
import traceback

import requests
from bs4 import BeautifulSoup
import psycopg2
from park_api import util, env

HEADERS = {
    "User-Agent": "ParkAPI v{} - Info: {}".format(env.SERVER_VERSION, env.SOURCE_REPOSITORY),
}


def get_html(city):
    """Download html data for a given city"""
    r = requests.get(city.data_url, headers=HEADERS)

    # Requests fails to correctly check the encoding for every site,
    # we're going to have to get that manually (in some cases). This sucks.
    soup = BeautifulSoup(r.text, "html.parser")
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


def _live(city):
    """
    Scrape data for a given city pulling all data now
    This function is only used in development mode for debugging the server without a database present.
    """
    return add_metadata(parse_html(city, get_html(city)))


def main():
    """Iterate over all cities in ./cities, scrape and save their data to the database"""

    conn = psycopg2.connect(**env.DATABASE)
    cursor = conn.cursor()

    for file, city in env.supported_cities().items():
        try:
            data = add_metadata(parse_html(city, get_html(city)))
            save_data_to_db(cursor, data, file.title())
        except Exception as e:
            print("Failed to scrape '%s': %s" %(city, e))
            print(traceback.format_exc())

    conn.commit()
    conn.close()
