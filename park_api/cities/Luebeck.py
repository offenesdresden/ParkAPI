from bs4 import BeautifulSoup
from park_api.util import convert_date, get_most_lots_from_known_data
from park_api.geodata import GeoData

data_url = "http://kwlpls.adiwidjaja.info"
data_source = "http://www.kwl-luebeck.de/parken/aktuelle-parkplatzbelegung/"
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
    soup = BeautifulSoup(html, "html.parser")

    date_field = soup.find("tr").find("strong").text
    last_updated = convert_date(date_field, "Stand: %d.%m.%Y, %H:%M Uhr")
    data = {
        "last_updated": last_updated,
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

            type_and_name = process_name(raw_lot_data[0].text)

            if len(raw_lot_data) == 2:
                total = get_most_lots_from_known_data("Lübeck", type_and_name[1])
                free = 0
                state = process_state_map.get(raw_lot_data[1].text, "")
            elif len(raw_lot_data) == 4:
                total = int(raw_lot_data[1].text)
                free = int(raw_lot_data[2].text)
                state = "open"

            lot = geodata.lot(type_and_name[1])
            data["lots"].append({
                "name": lot.name,
                "type": type_and_name[0],
                "total": total,
                "free": free,
                "region": region_header,
                "state": state,
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
    return type_mapping.get(lot_type, ""), lot_name
