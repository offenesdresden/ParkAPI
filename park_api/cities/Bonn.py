from bs4 import BeautifulSoup
from park_api.models import GeoData, Lots
from park_api.util import parse_date

geodata = GeoData(__file__)

lot_map = {
        0: "Münsterplatzgarage",
        1: "Stadthausgarage",
        2: "Beethoven-Parkhaus",
        3: "Bahnhofgarage",
        4: "Friedensplatzgarage",
        5: "Marktgarage",
        }


def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")

    free_lots = soup.find_all("td", class_="stell")
    assert len(free_lots) == 6, \
        "Expect to find 6 lots in Bonn, got: %d" % len(free_lots)
    time = soup.find("td", {"class": "stand"}).text.strip()

    lots = Lots()
    updated_at = parse_date(time, "%d.%m.%y %H:%M:%S")
    for idx, free in enumerate(free_lots):
        lot = geodata.lot(lot_map[idx])
        lot.free = int(free.text)
        lot.updated_at = updated_at
        lot.state = "nodata"
        lots.append(lot)

    return lots
