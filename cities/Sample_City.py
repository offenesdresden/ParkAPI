from bs4 import BeautifulSoup
import json
import datetime
import pytz

# The URL for the page where the parking lots are listed
data_url = "http://example.com"

# Name of the city, just in case it contains umlauts which this filename shouldn't
city_name = "Sample City"

# Name of this file (without '.py'), sorry for needing this, but it makes things easier
file_name = "Sample_City"


def parse_html(html):
    soup = BeautifulSoup(html)

    # Do everything necessary to scrape the contents of the html
    # into a dictionary of the format specified by the schema.


def get_geodata_for_lot(lot_name):
    geofile = open("./cities/" + file_name + ".geojson")
    geodata = geofile.read()
    geofile.close()
    geodata = json.loads(geodata)

    for feature in geodata["features"]:
        if feature["properties"]["name"] == lot_name:
            return {
                "lon": feature["geometry"]["coordinates"][0],
                "lat": feature["geometry"]["coordinates"][1]
            }
    return []


if __name__ == "__main__":
    file = open("../tests/sample_city.html")
    html_data = file.read()
    file.close()
    parse_html(html_data)
