from bs4 import BeautifulSoup
from park_api.util import convert_date
from park_api.geodata import GeoData

# This loads the geodata for this city if <city>.geojson exists in the same directory as this file.
# No need to remove this if there's no geodata (yet), everything will still work.
geodata = GeoData(__file__)

# This function is called by the scraper and given the data of the page specified as source in geojson above.
# It's supposed to return a dictionary containing everything the current spec expects. Tests will fail if it doesn't ;)
def parse_html(html):

    # BeautifulSoup is a great and easy way to parse the html and find the bits and pieces we're looking for.
    soup = BeautifulSoup(html, "html.parser")

    # last_updated is the date when the data on the page was last updated, it should be listed on most pages
    last_updated = soup.select("p#last_updated")[0].text

    data = {
        # convert_date is a utility function you can use to turn this date into the correct string format
        "last_updated": convert_date(last_updated, "%d.%m.%Y %H:%M Uhr"),
        # URL for the page where the scraper can gather the data
        "lots": []
    }

    for tr in soup.find_all("tr"):
        lot_name = tr.find("td", {"class": "lot_name"}).text
        lot_free = tr.find("td", {"class": "lot_free"}).text
        lot_total = tr.find("td", {"class": "lot_total"}).text

        # please be careful about the state only being allowed to contain either open, closed or nodata
        # should the page list other states, please map these into the three listed possibilities
        state = tr.find("td", {"class": "lot_state"}).text

        lot = geodata.lot(lot_name)
        data["lots"].append({
            "name": lot.name,
            "free": lot_free,
            "total": lot_total,
            "address": lot.address,
            "coords": lot.coords,
            "state": state,
            "type": lot.type,
            "id": lot.id,
            "forecast": False,
        })

    return data
