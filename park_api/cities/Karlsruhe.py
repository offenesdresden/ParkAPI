from bs4 import BeautifulSoup
from park_api.geodata import GeoData
from park_api.util import utc_now

# This loads the geodata for this city if <city>.geojson exists in the same directory as this file.
# No need to remove this if there's no geodata (yet), everything will still work.
geodata = GeoData(__file__)

# This function is called by the scraper and given the data of the page specified as source in geojson above.
# It's supposed to return a dictionary containing everything the current spec expects. Tests will fail if it doesn't ;)
def parse_html(html):

    # BeautifulSoup is a great and easy way to parse the html and find the bits and pieces we're looking for.
    soup = BeautifulSoup(html, "html.parser")

    # last update time (UTC)
    # Karlsruhe does not support the last_upted yet. 
    # as the data seems accurate I will return the current time and date
    data = {
        "last_updated": utc_now(),
        "lots": []
    }

    lots = soup.find_all( 'div', class_='parkhaus')
    for parking_lot in lots :
        parking_name = parking_lot.find('a').text
        lot = geodata.lot(parking_name)

        parking_state = 'open'
        parking_free = 0
        parking_fuellstand = parking_lot.find( 'div', class_='fuellstand')
        try :
            if ( parking_fuellstand == None ) :
                parking_state = 'nodata'
            else :
                temp= parking_fuellstand.text.split()
                parking_free = int(temp[0])
        except :
            parking_state = 'nodata' 

        data["lots"].append({
            "name": parking_name,
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
