#!/usr/bin/env python
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
    r = requests.get(city.source, headers=HEADERS)

    # Requests fails to correctly check the encoding for every site,
    # we're going to have to get that manually (in some cases). This sucks.
    soup = BeautifulSoup(r.text, "html.parser")
    meta_content = soup.find("meta", {"http-equiv": "content-type"})
    if meta_content is not None:
        encoding = meta_content["content"].split("=")[-1]
        r.encoding = encoding

    return r.text


def scrape_lots(module):
    html = get_html(module.geodata.city)
    lots = module.parse_html(html)
    lots.downloaded_at = util.utc_now()
    return lots


def main():
    """
    Iterate over all cities in ./cities,
    scrape and save their data to the database
    """
    db.setup()
    with db.cursor(commit=True) as cursor:
        # the catch-all enterprise loop
        for module in env.supported_cities().values():
            try:
                lots = scrape_lots(module)
                lots.save(cursor)
            except Exception as e:
                print("Failed to scrape '%s': %s" %
                      (module.geodata.city.name, e))
                print(traceback.format_exc())
