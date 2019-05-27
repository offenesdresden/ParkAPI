from bs4 import BeautifulSoup
from park_api.util import convert_date
from park_api.geodata import GeoData
import datetime
import json
import urllib
import random

# This loads the geodata for this city if <city>.geojson exists in the same directory as this file.
# No need to remove this if there's no geodata (yet), everything will still work.
geodata = GeoData(__file__)

# This function is called by the scraper and given the data of the page specified as source in geojson above.
# It's supposed to return a dictionary containing everything the current spec expects. Tests will fail if it doesn't ;)
def parse_html(html):

    # BeautifulSoup is a great and easy way to parse the html and find the bits and pieces we're looking for.
    # soup = BeautifulSoup(html, "html.parser")

    # read the JSON-file:
    #      URL + no caching
    urlHD = "http://parken.heidelberg.de/api-v1/parking-location?api_key=H5WaIyR4lgn6wzo7rJf8u4ubecgpX0Q8&nc="+str(random.random())
    headerHD={'Accept': 'application/json; charset=utf8'}
    req = urllib.request.Request(url=urlHD, headers=headerHD)
    webURL = urllib.request.urlopen(req)
    data=webURL.read()
    dataJSON=json.loads(data)

    # last_updated is the date when the data on the page was last updated, it should be listed on most pages
    date_time_temp = dataJSON['data']['updated']
    last_updated   = datetime.datetime.strptime(date_time_temp, '%a, %d %b %Y %H:%M:%S %z')
    
    data = {
        # convert_date is a utility function you can use to turn this date into the correct string format
        "last_updated": convert_date(last_updated, "%d.%m.%Y %H:%M Uhr"),
        # URL for the page where the scraper can gather the data
        "lots": []
    }

    # iteration over single parking_lots
    for parking_lot in dataJSON['data']['parkinglocations'] :
        # please keep the name in the geojson-file in the same form as delivered here (including spaces)
        parking_name = 'P'+str(parking_lot['uid'])+' '+parking_lot['name']
        # get the data
        lot = geodata.lot(parking_name)

        parking_state = 'open'
        parking_free = 0
        if ( parking_lot['parkingupdate']['status'] == 'closed' ) :
            parking_state = 'closed'
        else :
            parking_free = int(parking_lot['parkingupdate']['total']) - int(parking_lot['parkingupdate']['current'])
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
