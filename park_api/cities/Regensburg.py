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
    #   suche: <p class="updateinfo">zuletzt aktualisiert: 28.05.2019 15.30 Uhr</p>
    updated = soup.find( "p", class_="updateinfo")
    last_updated = convert_date(updated.text, 'zuletzt aktualisiert: %d.%m.%Y %H.%M Uhr')

    data = {
        "last_updated": last_updated,
        # URL for the page where the scraper can gather the data
        "lots": []
    }

    parking_lots = soup.find_all("div", class_="accordeon parkmoeglichkeit")
    for one_lot in parking_lots :
        parking_name = one_lot.find("h3").text
        lot = geodata.lot(parking_name)

        parking_state = 'open'
        parking_free = 0
        parking_belegung = one_lot.find("div", class_="belegung")
        if (parking_belegung != None ) :
            parking_free=int(parking_belegung.find("strong").text)
        else:
            parking_state='nodata'

        data["lots"].append({
            "name": lot.name,
            "free": parking_free,
            "total": lot.total,
            "address": lot.address,
            "coords": lot.coords,
            "state": parking_state,
            "lot_type": lot.type,
            "id": lot.id,
            "forecast": False,
        })

    return data
