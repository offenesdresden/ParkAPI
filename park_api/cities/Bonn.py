from bs4 import BeautifulSoup
from park_api.geodata import GeoData
from park_api.util import convert_date, generate_id

data_url = "http://www.bcp-bonn.de/bspspinfo1.php"
data_source = "http://www.bcp-bonn.de/bcp/index.php?id=80"
city_name = "Bonn"

class Lot:
    def __init__(self, name, total, address):
        self.name = name
        self.total = total
        self.address = address


lot_map = {
    0: Lot("Münsterplatzgarage", 319, "Budapester Straße"),
    1: Lot("Stadthausgarage", 300, "Weiherstraße"),
    2: Lot("Beethoven-Parkhaus", 426, "Engeltalstraße"),
    3: Lot("Bahnhofgarage", 110, " Münsterstraße"),
    4: Lot("Friedensplatzgarage", 822, "Oxfordstraße"),
    5: Lot("Marktgarage", 325, "Stockenstraße"),
}
geodata = GeoData(__file__)


def parse_html(html):
    soup = BeautifulSoup(html)

    free_lots = soup.find_all("td", {"class": "stell"})
    assert len(free_lots) == 6, "Expect to find 6 lots in Bonn, got: %d" % len(free_lots)
    time = soup.find("td", {"class": "stand"}).text.strip()

    lots = []
    for idx, free in enumerate(free_lots):
        lot = lot_map.get(idx)
        lots.append({
            "name": lot.name,
            "coords": geodata.coords(lot.name),
            "free": int(free.text),
            "address": lot.address,
            "total": lot.total,
            "state": "nodata",
            "id": generate_id(__file__, lot.name),
            "forecast": False
        })

    return {
        "last_updated": convert_date(time, "%d.%m.%y %H:%M:%S"),
        "data_source": data_source,
        "lots": lots
    }
