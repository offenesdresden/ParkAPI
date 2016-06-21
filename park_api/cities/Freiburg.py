from park_api.util import convert_date
from park_api.geodata import GeoData
import json

# This loads the geodata for this city if <city>.geojson exists in the same directory as this file.
# No need to remove this if there's no geodata (yet), everything will still work.
geodata = GeoData(__file__)

# This function is called by the scraper and given the data of the page specified as source in geojson above.
# It's supposed to return a dictionary containing everything the current spec expects. Tests will fail if it doesn't ;)
def parse_html(source_json):

    parsed_json = json.loads(source_json)
    features = parsed_json['features']

    # last_updated is the date when the data on the page was last updated, it should be listed on most pages
    last_updated = ""

    data = {
        # URL for the page where the scraper can gather the data
        "lots": []
    }

    for feature in features:
        lot_name = feature['properties']['park_name']
        lot_free = int(feature['properties']['obs_free'])
        lot_total = int(feature['properties']['obs_max'])

        if last_updated < feature['properties']['obs_ts']:
            last_updated = feature['properties']['obs_ts']

        # please be careful about the state only being allowed to contain either open, closed or nodata
        # should the page list other states, please map these into the three listed possibilities
        state = "nodata"

        if feature['properties']['obs_state'] == "1":
            state = "open"
        elif feature['properties']['obs_state'] == "0":
            state = "closed"

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

    data['last_updated'] = convert_date(last_updated, "%Y-%m-%d %H:%M:%S")

    return data
