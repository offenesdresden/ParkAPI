#!/usr/bin/env python
import json
import traceback

import requests
from bs4 import BeautifulSoup
from park_api import util, env, db

HEADERS = {
    "User-Agent": "ParkAPI v%s - Info: %s" %
    (env.SERVER_VERSION, env.SOURCE_REPOSITORY),
}


def get_html(city):
    """Download html data for a given city"""
    r = requests.get(city.source, headers={**HEADERS, **city.headers})

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
    sql = """
    INSERT INTO parkapi(
                timestamp_updated,
                timestamp_downloaded,
                city,
                data)
        VALUES (%(updated)s, %(downloaded)s, %(city)s, %(data)s)
        RETURNING 'id';
    """
    cursor.execute(sql, {
        "updated": timestamp_updated,
        "downloaded": timestamp_downloaded,
        "city": city,
        "data": json_data
    })

    print("Saved " + city + " to DB.")


def _live(module):
    """
    Scrape data for a given city pulling all data now
    This function is only used in development mode
    for debugging the server without a database present.
    """
    return add_metadata(module.parse_html(get_html(module.geodata.city)))


def scrape_city(module):
    city = module.geodata.city
    data = add_metadata(module.parse_html(get_html(city)))
    with db.cursor(commit=True) as cursor:
        save_data_to_db(cursor, data, city.id)


def main():
    """
    Iterate over all cities in ./cities,
    scrape and save their data to the database
    """
    # the catch-all enterprise loop
    db.setup()
    for module in env.supported_cities().values():
        try:
            scrape_city(module)
        except Exception as e:
            print("Failed to scrape '%s': %s" %
                  (module.geodata.city.name, e))
            print(traceback.format_exc())
