from bs4 import BeautifulSoup
from park_api.util import parse_date
from park_api.models import GeoData, Lots

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

    rows = soup.find_all("tr")
    rows = rows[1:]
    region_header = ""

    lots = Lots()
    updated_at = parse_date(date_field, "Stand: %d.%m.%Y, %H:%M Uhr")
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
            lot = geodata.lot(type_and_name[1])

            if len(raw_lot_data) == 2:
                lot.state = process_state_map.get(raw_lot_data[1].text, "")
            elif len(raw_lot_data) == 4:
                lot.total = int(raw_lot_data[1].text)
                lot.free = int(raw_lot_data[2].text)
                lot.state = "open"

            lot.lot_type = type_and_name[0]
            lot.region = region_header
            lot.updated_at = updated_at
            lots.append(lot)
    return lots


def process_name(name):
    lot_type = name[:2]
    lot_name = name[3:]

    type_mapping = {
        "PP": "Parkplatz",
        "PH": "Parkhaus",
    }
    return type_mapping.get(lot_type, ""), lot_name
