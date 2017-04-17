from bs4 import BeautifulSoup
from park_api.geodata import GeoData
from park_api.util import convert_date
import re
import datetime

geodata = GeoData(__file__)

lot_map = {
        0: "Anger 1",
        1: "Thomaseck",
        2: "Forum 1",
        3: "Forum 2+3",
        4: "Thüringenhaus",
        5: "Domplatz",
        6: "Hauptbahnhof",
        7: "Sparkassen-Finanzzentrum"
        }


def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    
    # get page
    m = re.findall(r'Ob(.*von.*);', html)
    time = str(datetime.datetime.now())
    lots_tmp = {}
    
    for elem in m:
        name = re.search(r'"[ A-Za-zöüä\xfc0-9+-]+"', elem,
                             re.UNICODE).group(0)[1:-1]
        belegt = re.search(r'[\-0-9]+\)', elem).group(0)[0:-1]
        max = re.search(r'von.*,', elem).group(0)[5:-1]
        lots_tmp[name] = {"free": str(int(max)-int(belegt))}

    assert len(m) == 8, \
        "Expect to find 8 lots in Erfurt, got: %d" % len(m)

    lots = []
    for idx, free in enumerate(m):
        lot = geodata.lot(lot_map[idx])
        lots.append({
            "name": lot.name,
            "coords": lot.coords,
            "free": int(lots_tmp.get(name).get("free")),
            "address": lot.address,
            "total": lot.total,
            "state": "nodata",
            "id": lot.id,
            "forecast": False
        })

    return {
        "last_updated": convert_date(time.split('.')[0], "%Y-%m-%d %H:%M:%S"),
        "lots": lots
    }
