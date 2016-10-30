from park_api.util import convert_date
from park_api.geodata import GeoData
from datetime import datetime
import json
import re

# This loads the geodata for this city if <city>.geojson exists in the same directory as this file.
geodata = GeoData(__file__)


def parse_html(text_content):
    # the original JSON is invalid, let's fix it
    p = re.compile(r'([^"]|\s)([a-zA-Z]+)\s?(:)')
    text_content = text_content.replace("'", "\"")
    text_content = re.sub(p, r'\1"\2"\3', text_content)
    data_as_json = json.loads(text_content)

    # the source doesn't publish the update time, so we assume present
    last_updated = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    data = {
        "last_updated": convert_date(last_updated, "%Y/%m/%d %H:%M:%S"),
        "lots": []
    }

    state_mappings = {
        1: "open",
        0: "closed"
    }

    for record in data_as_json["parkPlacesAreaMarkers"]:
        lot_name = record["Name"]
        free = int(record["FreeCount"])
        total = int(record["MaxCount"])

        # the JSON file contains parking lots for which counting does work, let's ignore them
        if total > 0:
            latitude = record["Latitude"]
            longitude = record["Longitude"]
            state_key = int(record["IsOpen"])
            state = state_mappings[state_key]

            lot = geodata.lot(lot_name)
            data["lots"].append({
                "name": lot_name,
                "free": free,
                "total": total,
                "address": lot.address,
                "coords": lot.coords,
                "state": state,
                "lot_type": lot.type,
                "id": lot.id,
                "forecast": False,
            })

    return data
