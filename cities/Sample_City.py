from bs4 import BeautifulSoup
from util import convert_date, generate_id
from geodata import GeoData

# URL for the page where the scraper can gather the data
data_url = "http://example.com/parkingdata"

# URL that is displayed as the source of this data, usually the domain of the URL above
data_source = "http://example.com"

# Name of the city, just in case it contains umlauts which this filename shouldn't
city_name = "Sample City"

# Name of this file (without '.py'), sorry for needing this, but it makes things easier
file_name = "Sample_City"

# Uncomment the following line if there's geodata in the format of Sample_City.geodata in this directory
geodata = GeoData(__file__)


def parse_html(html):
    soup = BeautifulSoup(html)

    # Do everything necessary to scrape the contents of the html
    # into a dictionary of the format specified by the schema.

    last_updated = soup.select("p#last_updated")[0].text

    data = {
        # last_updated is the date when the data on the page was last updated, it should be listed on most pages
        # convert_date is a utility function you can use to turn this date into the correct string format
        "last_updated": convert_date(last_updated, "%d.%m.%Y %H:%M Uhr"),
        "data_source": data_source,
        "lots": []
    }

    for tr in soup.find_all("tr"):
        lot_name = tr.find("td", {"class": "lot_name"}).text
        lot_free = tr.find("td", {"class": "lot_free"}).text
        lot_total = tr.find("td", {"class": "lot_total"}).text
        lot_address = tr.find("td", {"class": "lot_address"}).text
        lot_type = tr.find("td", {"class": "lot_type"}).text

        # please be careful about the state only being allowed to contain either open, closed or nodata
        # should the page list other states, please map these into the three listed possibilities
        state = tr.find("td", {"class": "lot_state"}).text

        data["lots"].append({
            "name": lot_name,
            "free": lot_free,
            "total": lot_total,
            "address": lot_address,
            "coords": geodata.coords(lot_name),
            "state": state,
            "type": lot_type,
            # use the utility function generate_id to generate an ID for this lot
            # it takes this file path and the lot's name as params
            "id": generate_id(__file__, lot_name),
            "forecast": False,
        })

    return data
