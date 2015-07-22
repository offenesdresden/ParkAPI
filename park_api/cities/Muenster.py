from bs4 import BeautifulSoup
from park_api.util import convert_date
from park_api.geodata import GeoData

data_url = "http://www5.stadt-muenster.de/parkhaeuser/"
data_source = "http://www5.stadt-muenster.de/parkhaeuser/"
city_name = "Münster"

state_map = {
    "frei": "open",
    "geschlossen": "closed",
    "besetzt": "open"
}

geodata = GeoData(__file__)

def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")

    lot_table_trs = soup.select("div#parkingList table")[0].find_all("tr")
    date_field = soup.find(id="lastRefresh").text.strip()

    data = {
        "last_updated": convert_date(date_field, "%d.%m.%Y %H:%M Uhr"),
        "data_source": data_source,
        "lots": []
    }

    for tr in lot_table_trs[1:-1]:
        tds = tr.find_all("td")
        type_and_name = process_name(tds[0].text)
        lot = geodata.lot(type_and_name[1])
        data["lots"].append({
            "name": lot.name,
            "type": type_and_name[0],
            "free": int(tds[1].text),
            "total": lot.total,
            "state": state_map.get(tds[2].text, ""),
            "coords": lot.coords,
            "id": lot.id,
            "forecast": False
        })

    return data


def process_name(name):
    lot_type = name[:2]
    lot_name = name[3:]

    type_mapping = {
        "PP": "Parkplatz",
        "PH": "Parkhaus",
    }
    if lot_type in type_mapping.keys():
        lot_type = type_mapping[lot_type]
    else:
        lot_type = ""
        lot_name = name

    return lot_type, lot_name
