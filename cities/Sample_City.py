from bs4 import BeautifulSoup
from util import convert_date
from geodata import GeoData

# The URL for the page where the parking lots are listed
data_url = "http://example.com"

# Name of the city, just in case it contains umlauts which this filename shouldn't
city_name = "Sample City"

# Name of this file (without '.py'), sorry for needing this, but it makes things easier
file_name = "Sample_City"

# Uncomment the following line if there's geodata in the format of Sample_City.geodata in this directory
# geodata = GeoData(city_name)

def parse_html(html):
    soup = BeautifulSoup(html)

    # Do everything necessary to scrape the contents of the html
    # into a dictionary of the format specified by the schema.

    data = {
        "last_updated": convert_date("date_string", "date_format"),
        "lots": []
    }

    return data

# the following is for testing this out, just delete it all when done
if __name__ == "__main__":
    with open("../tests/fixtures/" + file_name.lower() + ".html") as f:
        parse_html(f.read())
