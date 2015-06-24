from bs4 import BeautifulSoup
from geodata import GeoData
from util import convert_date

data_url = "http://www.bcp-bonn.de/bspspinfo1.php"
data_source = "http://www.bcp-bonn.de/bcp/"
city_name = "Bonn"
file_name = "Bonn"

class Lot:
    def __init__(self, name, count, address):
        self.name = name
        self.count = count
        self.address = address
lot_map = {
    0: Lot("Münsterplatzgarage", 319, "Budapester Straße"),
    1: Lot("Stadthausgarage", 300, "Weiherstraße"),
    2: Lot("Beethoven-Parkhaus", 426, "Engeltalstraße"),
    3: Lot("Bahnhofgarage", 110, " Münsterstraße"),
    4: Lot("Friedensplatzgarage", 822, "Oxfordstraße"),
    5: Lot("Marktgarage", 325, "Stockenstraße"),
}
geodata = GeoData(city_name)

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
            "count": lot.count
        })

    return {
            "last_updated": convert_date(time, "%d.%m.%y %H:%M:%S"),
            "lots": lots
    }
