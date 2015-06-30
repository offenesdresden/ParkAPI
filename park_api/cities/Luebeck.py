from bs4 import BeautifulSoup
from park_api.util import convert_date, generate_id
from park_api.geodata import GeoData

data_url = "http://kwlpls.adiwidjaja.info"
data_source = "http://www.kwl-luebeck.de"
city_name = "Lübeck"

process_state_map = {
    "": "open",
    "Geöffnet": "open",
    "Vorübergehend geschlossen.": "closed",
    "Vorübergehend geschlossen": "closed",
    "Geschlossen": "closed"
}

geodata = GeoData(__file__)


def parse_html(html):
    soup = BeautifulSoup(html)

    data = {
        "last_updated": convert_date(soup.find("tr").find("strong").text, "Stand: %d.%m.%Y, %H:%M Uhr"),
        "data_source": data_source,
        "lots": []
    }

    rows = soup.find_all("tr")
    rows = rows[1:]
    region_header = ""

    for row in rows:
        if len(row.find_all("th")) > 0:
            # This is a header row, save it for later
            region_header = row.find("th", {"class": "head1"}).text

        else:
            if row.find("td").text == "Gesamt":
                continue

            # This is a parking lot row
            raw_lot_data = row.find_all("td")

            if len(raw_lot_data) == 2:
                type_and_name = process_name(raw_lot_data[0].text)
                data["lots"].append({
                    "name": type_and_name[1],
                    "type": type_and_name[0],
                    "total": 0,
                    "free": 0,
                    "region": region_header,
                    "state": process_state_map.get(raw_lot_data[1].text, ""),
                    "coords": geodata.coords(type_and_name[1]),
                    "id": generate_id(__file__, type_and_name[1]),
                    "forecast": False
                })

            elif len(raw_lot_data) == 4:
                type_and_name = process_name(raw_lot_data[0].text)
                data["lots"].append({
                    "name": type_and_name[1],
                    "type": type_and_name[0],
                    "total": int(raw_lot_data[1].text),
                    "free": int(raw_lot_data[2].text),
                    "region": region_header,
                    "state": "open",
                    "coords": geodata.coords(type_and_name[1]),
                    "id": generate_id(__file__, type_and_name[1]),
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

    return lot_type, lot_name
