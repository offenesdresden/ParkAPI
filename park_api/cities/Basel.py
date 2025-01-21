import json
from datetime import datetime
from datetime import timezone
from park_api.geodata import GeoData

geodata = GeoData(__file__)


def parse_html(xml_data):
    feed = json.loads(xml_data)

    last_updated = feed['results'][0]['published']
    last_updated = last_updated[:-3] + last_updated[-2:]
    last_updated = datetime.strptime(last_updated, '%Y-%m-%dT%H:%M:%S%z').astimezone(timezone.utc).isoformat()[:-6]

    data = {
        "lots": [],
        "last_updated": last_updated
    }

    for entry in feed['results']:

        data["lots"].append({
            "name": entry['name'],
            "address": entry['address'],
            "id": entry['id'],
            "state": translate_status(entry['status']),
            "free": entry['free'],
            "total": entry['total'],
            "coords": list(entry['geo_point_2d'].values()),
            "forecast": False,
            "lot_type": entry['lot_type']
        })

    return data

def translate_status(status: str) -> str:
    state = None

    if status == 'offen':
        state = 'open'
    elif status == 'zu':
        state = 'closed'
    else:
        state = 'unknown state'

    return state
