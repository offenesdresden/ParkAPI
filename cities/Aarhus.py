from bs4 import BeautifulSoup
from park_api.util import convert_date
from park_api.geodata import GeoData
import json

# This loads the geodata for this city if <city>.geojson exists in the same directory as this file.
geodata = GeoData(__file__)


def parse_html(text_content):
    data_as_json = json.loads(text_content)

    # last_updated is the date when the data on the page was last updated, it should be listed on most pages
    last_updated = data_as_json["result"]["records"][0]["date"]
    data = {
        "last_updated": convert_date(last_updated, "%Y/%m/%d %H:%M:%S"),
        "lots": []
    }

    # The page at https://www.odaa.dk/dataset/parkeringshuse-i-aarhus describes how the counts are made
    map_json_names = {
        "NORREPORT": "Nørreport",
        # "SKOLEBAKKEN": None,
        "SCANDCENTER": "Scandinavian Center",
        "BRUUNS": "Bruuns Galleri",
        "MAGASIN": "Magasin",
        "KALKVAERKSVEJ": "Kalkværksvej",
        "SALLING": "Salling",
        "Navitas": "Navitas",
        "NewBusgadehuset": "Busgadehuset"
    }

    cummulatives = {
        "Urban Level 1": "Dokk1",
        "Urban Level 2+3": "Dokk1"
    }

    cumulative_lots = {}

    for record in data_as_json["result"]["records"]:
        lot_code = record["garageCode"]
        total = int(record["totalSpaces"])
        free = max(int(record["totalSpaces"]) - int(record["vehicleCount"]), 0)

        if lot_code not in map_json_names.keys() and lot_code not in cummulatives.keys():
            continue
        elif lot_code in map_json_names.keys():
            lot_name = map_json_names[lot_code]
            lot = geodata.lot(lot_name)
            data["lots"].append({
                "name": lot_name,
                "free": free,
                "total": total,
                "address": lot.address,
                "coords": lot.coords,
                "state": "unknown",
                "lot_type": lot.type,
                "id": lot.id,
                "forecast": False,
            })
        elif lot_code not in cummulatives.keys():
            lot_name = cummulatives[lot_code]
            if lot_name not in cumulative_lots.keys():
                cumulative_lots[lot_name] = {
                    "name": lot_name,
                    "free": free,
                    "total": total,
                    "address": lot.address,
                    "coords": lot.coords,
                    "state": "unknown",
                    "lot_type": lot.type,
                    "id": lot.id,
                    "forecast": False,
                }
            else:
                current_data = cumulative_lots[lot_name]
                cumulative_lots[lot_name] = {
                    "name": lot_name,
                    "free": current_data["free"] + free,
                    "total": current_data["total"] + total,
                    "address": lot.address,
                    "coords": lot.coords,
                    "state": "unknown",
                    "lot_type": lot.type,
                    "id": lot.id,
                    "forecast": False,
                }

    for lot in cumulative_lots:
        data["lots"].append(lot)

    return data
