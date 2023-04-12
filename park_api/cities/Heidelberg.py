from bs4 import BeautifulSoup
from park_api.util import convert_date
from park_api.geodata import GeoData
import json
from park_api import env

# This loads the geodata for this city if <city>.geojson exists in the same directory as this file.
# No need to remove this if there's no geodata (yet), everything will still work.
geodata = GeoData(__file__)

# This function is called by the scraper and given the data of the page specified as source in geojson above.
# It's supposed to return a dictionary containing everything the current spec expects. Tests will fail if it doesn't ;)
def parse_html(html):

    dataJSON=json.loads(html)

    data = {
        # convert_date is a utility function you can use to turn this date into the correct string format
        "last_updated": convert_date(dataJSON['data']['updated'].split("+")[0][:-1], '%a, %d %b %Y %H:%M:%S'),
        # URL for the page where the scraper can gather the data
        "lots": []
    }

    # iteration over single parking_lots
    for parking_lot in dataJSON['data']['parkinglocations'] :
        # please keep the name in the geojson-file in the same form as delivered here (including spaces)
        parking_name = 'P'+str(parking_lot['uid'])+' '+parking_lot['name']
        # get the data
        lot = geodata.lot(parking_name)
        
        parking_total = int(parking_lot['parkingupdate']['total'])
        parking_state = 'open'
        parking_free = 0
        try :
            if ( parking_lot['parkingupdate']['status'] == 'closed' ) :
                parking_state = 'closed'
            else :
                parking_free = int(parking_lot['parkingupdate']['total']) - int(parking_lot['parkingupdate']['current'])
        except :
            parking_state = 'nodata'

        data["lots"].append({
            "name": parking_name,
            "free": parking_free,
            "total": parking_total,
            "address": lot.address,
            "coords": lot.coords,
            "state": parking_state,
            "lot_type": lot.type,
            "id": lot.id,
            "forecast": False,
        })

    return data
