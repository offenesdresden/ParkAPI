from bs4 import BeautifulSoup
from park_api.util import parse_date
from park_api.models import GeoData, Lots

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

    lots = Lots()
    updated_at = parse_date(date_field, "%d.%m.%Y %H:%M Uhr")
    for tr in lot_table_trs[1:-1]:
        tds = tr.find_all("td")
        description = tds[0].text.strip()
        type_, name = process_name(description)
        lot = geodata.lot(description)
        lot.name = type_.strip("\n")
        lot.lot_type = name[0]
        lot.free = int(tds[1].text)
        lot.state = state_map.get(tds[2].text, "")
        lot.updated_at = updated_at
        lots.append(lot)
    return lots


def process_name(name):
    lot_type = name[:3].strip()
    lot_name = name[3:].strip()

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
