from datetime import datetime

from bs4 import BeautifulSoup

from park_api.geodata import GeoData
from park_api.util import utc_now

# This loads the geodata for this city if <city>.geojson exists in the same directory as this file.
# No need to remove this if there's no geodata (yet), everything will still work.
geodata = GeoData(__file__)


# This function is called by the scraper and given the data of the page specified as source in geojson above.
# It's supposed to return a dictionary containing everything the current spec expects. Tests will fail if it doesn't ;)

def parse_html(xml):
    soup = BeautifulSoup(xml, "html.parser")

    # last_updated is the date when the data on the page was last updated, it should be listed on most pages

    try:
        last_updated = soup.select("zeitstempel")[0].text
    except KeyError:
        last_updated = utc_now()

    data = {
        # convert_date is a utility function you can use to turn this date into the correct string format
        "last_updated": datetime.strptime(last_updated[0:16], "%d.%m.%Y %H:%M").isoformat(),
        # URL for the page where the scraper can gather the data
        "lots": []
    }

    for ph in soup.find_all("parkhaus"):
        lot_name = ph.find("name").text
        lot_actual = int(ph.find("aktuell").text)
        lot_total = int(ph.find("gesamt").text)
        lot_free = lot_total - lot_actual

        # please be careful about the state only being allowed to contain either open, closed or nodata
        # should the page list other states, please map these into the three listed possibilities
        # translate german state to english
        stateGerman = ph.find("status").text
        if stateGerman == ("Offen"):
            state = "open"
        elif stateGerman == ("Geschlossen"):
            state = "closed"
        else:
            state = "nodata"

        lot = geodata.lot(lot_name)
        data["lots"].append({
            "name": lot.name,
            "free": lot_free,
            "total": lot_total,
            "address": lot.address,
            "coords": lot.coords,
            "state": state,
            "lot_type": lot.type,
            "id": lot.id,
            "forecast": False,
        })

    return data
