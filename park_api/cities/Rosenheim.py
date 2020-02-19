from bs4 import BeautifulSoup
from park_api.geodata import GeoData
from park_api.util import utc_now
from park_api import env
import json

# This loads the geodata for this city if <city>.geojson exists in the same directory as this file.
# No need to remove this if there's no geodata (yet), everything will still work.
geodata = GeoData(__file__)

# This function is called by the scraper and given the data of the page specified as source in geojson above.
# It's supposed to return a dictionary containing everything the current spec expects. Tests will fail if it doesn't ;)
def parse_html(html):

    data = {
        "last_updated": utc_now(),     # not found on site, so we use something else
        # URL for the page where the scraper can gather the data
        "lots": []
    }

    dataJSON=json.loads(html)
    # over all parking-lots
    for parking_lot in dataJSON :
        parking_name = parking_lot['title']
        if ( parking_name != 'Reserve' ) :
            lot = geodata.lot(parking_name)
            try :
                parking_free = 0
                if ( parking_lot['isOpened'] == False) :
                    parking_status = 'closed'
                else :
                    parking_status = 'open'
                    parking_free = int(parking_lot['free'])
            except :
                parking_status = 'nodata'
            data["lots"].append({
                    "name":     parking_name,
                    "free":     parking_free,
                    "total":    parking_lot['parkings'],
                    "address":  lot.address,
                    "coords":   lot.coords,
                    "state":    parking_status,
                    "lot_type": lot.type,
                    "id":       lot.id,
                    "forecast": False
                })

    return data

