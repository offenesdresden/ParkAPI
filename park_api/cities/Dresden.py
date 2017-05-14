import os
import json
import time
import datetime
from park_api.geodata import GeoData
from park_api.util import convert_date, get_most_lots_from_known_data

geodata = GeoData(__file__)


def parse_html(html):
    if geodata.private_data:
        api_data = json.loads(html)
        dt = time.strptime(api_data[0]["timestamp"].split(".")[0], "%Y-%m-%dT%H:%M:%S")
        ts = time.gmtime(time.mktime(dt))
        data = {
            "lots": [],
            "last_updated": time.strftime("%Y-%m-%dT%H:%M:%S", ts)
        }
        status = ['open', 'closed', 'unknown']
        id_lots = {geodata.lots[n].aux: geodata.lots[n] for n in geodata.lots}
        for dataset in api_data:
            print(dataset)
            try:
                lot = id_lots[dataset['id']]
                forecast = os.path.isfile("forecast_data/" + lot.id + ".csv")
                data["lots"].append({
                    "coords": lot.coords,
                    "name": lot.name,
                    "total": lot.total,
                    "free": max(lot.total - dataset["belegung"], 0),
                    "state": status[dataset["status"] - 1],
                    "id": lot.id,
                    "lot_type": lot.type,
                    "address": lot.address,
                    "forecast": forecast,
                    "region": ""
                })
            except:
                pass
    else:
        #TODO: implement alternative if another API is used.
        data = {
            "lots": [],
            "last_updated": ""
        }

    return data
