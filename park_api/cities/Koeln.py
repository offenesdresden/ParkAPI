import json
import datetime
from park_api.util import convert_date
from park_api.geodata import GeoData

# This loads the geodata for this city if <city>.geojson exists in the same directory as this file.
# No need to remove this if there's no geodata (yet), everything will still work.
geodata = GeoData(__file__)

# This function is called by the scraper and given the data of the page specified as source in geojson above.
# It's supposed to return a dictionary containing everything the current spec expects. Tests will fail if it doesn't ;)
def parse_html(html):
    data = json.loads(html)
    lots = {
            "lots":[],
            "last_updated":None
            }
    id_lots = {geodata.lots[n].aux: geodata.lots[n] for n in geodata.lots}
    timestamps = []
    for feature in data["features"]:
        try:
            lot = id_lots[feature["attributes"]["IDENTIFIER"]]
            lots["lots"].append({
                "coords":lot.coords,
                "name":lot.name,
                "total":lot.total,
                "free":feature["attributes"]["KAPAZITAET"],
                "state":"nodata" if feature["attributes"]["KAPAZITAET"] == -1 else "open",
                "id":lot.id,
                "lot_type":lot.type,
                "address":lot.address,
                "forecast":False,
                "region":""
            })
            timestamps.append(convert_date(feature["attributes"]["TIMESTAMP"], "%Y-%m-%d %H:%M:%S"))
        except KeyError:
            pass
    timestamps.sort()
    timestamps.reverse()
    lots["last_updated"] = timestamps[0]
    return lots

