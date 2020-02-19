from park_api.util import convert_date
from park_api.geodata import GeoData
from datetime import datetime
import json
import re

# This loads the geodata for this city if <city>.geojson exists in the same directory as this file.
geodata = GeoData(__file__)


def parse_html(text_content):

    elems = text_content.split("\r\n\r\n")

    data = {
        "last_updated": convert_date(elems[0], "%d-%m-%Y %H:%M:%S "),
        "lots": []
    }

    state_mappings = {
        1: "open",
        0: "closed"
    }

    for elem in elems[1:]:
        e = {"name": elem.split("\r\n")[0].split("=")[1],
             "free": int(elem.split("\r\n")[1].split("=")[1])}
        lot = geodata.lot(e["name"])
        data["lots"].append({
            "name": e["name"],
            "free": e["free"],
            "total": lot.total,
            "address": lot.address,
            "coords": lot.coords,
            "state": "unknown",
            "lot_type": lot.type,
            "id": lot.id,
            "forecast": False,
        })

    return data
