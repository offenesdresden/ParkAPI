from bs4 import BeautifulSoup
from park_api.util import convert_date
from park_api.geodata import GeoData

# This loads the geodata for this city if <city>.geojson
# exists in the same directory as this file.
# No need to remove this if there's no geodata (yet),
# everything will still work.
geodata = GeoData(__file__)


# This function is called by the scraper and
# given the data of the page specified as data_url above.
# It's supposed to return a dictionary,
# containing everything the current spec expects.
# Tests will fail if it doesn't ;)
def parse_html(html):
    # BeautifulSoup is a great and easy way to parse the html and
    # find the bits and pieces we're looking for.
    soup = BeautifulSoup(html, "html.parser")

    # last_updated is the date when the data on the page was last updated
    last_updated = str(soup.select("body"))
    start = str.find(last_updated, "Letzte Aktualisierung:") + 23
    last_updated = last_updated[start:start + 16]

    data = {
        # convert_date is a utility function
        # you can use to turn this date into the correct string format
        "last_updated": convert_date(last_updated, "%d.%m.%Y %H:%M"),
        "lots": []
    }

    status_map = {
        "Offen": "open",
        "Geschlossen": "closed"
    }

    for tr in soup.find_all("tr"):
        if tr.td is None:
            continue
        td = tr.findAll('td')
        parking_name = td[0].string
        # work-around for the Umlaute-problem: ugly but working
        if ( 'Heiligengeist-' in parking_name) : parking_name = 'Heiligengeist-Höfe'
        elif ( 'Schlossh' in parking_name) : parking_name = 'Schlosshöfe'
        # get the data
        lot = geodata.lot(parking_name)
        try:
            parking_state = 'open'
            parking_free  = 0
            if ( 'Geschlossen' in td[3].text ) : 
                parking_state = 'closed'
            else :
                parking_free = int(td[1].text)
        except:
            parking_state = 'nodata'

        data["lots"].append({
            "name":     parking_name,
            "free":     parking_free,
            "total":    lot.total,
            "address":  lot.address,
            "coords":   lot.coords,
            "state":    parking_state,
            "lot_type": lot.type,
            "id":       lot.id,
            "forecast": False
        })

    return data
