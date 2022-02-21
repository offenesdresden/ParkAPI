from bs4 import BeautifulSoup
from park_api.geodata import GeoData
from park_api.util import utc_now

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

    lots = []

    for row in soup.find_all("div", class_='parking-lots'):
        entity_wrapper_class = 'wpb_column vc_column_container vc_col-sm-3'
        for column in row.find_all("div", class_=entity_wrapper_class):
            h3 = column.find_all("h3")
            if not h3[0].a is None and len(h3) > 1:
                name = h3[0].a.string
                free = 0
                for heading in h3:
                    for heading_element in heading.find_all("span"):
                        if heading_element.find("strong") is not None:
                            free = int(heading_element.strong.get_text())
                lot = geodata.lot(name)
                ltype = None
                for p in [pt for pt in ["Parkhaus", "Parkplatz"] if pt in name]:
                    ltype = p
                lots.append({
                    "name": name,
                    "coords": lot.coords,
                    "free": free,
                    "address": lot.address,
                    "total": lot.total,
                    "state": "unknown",
                    "id": lot.id,
                    "lot_type": ltype,
                    "forecast": False
                })

            elif h3[0].string:
                name = h3[0].string
                ltype = None
                if "Parkhaus" in name:
                    ltype = "Parkhaus"
                elif "Parkplatz" in name:
                    ltype = "Parkplatz"
                lot = geodata.lot(name)
                lots.append({
                    "name": name,
                    "coords": lot.coords,
                    "free": 0,
                    "address": lot.address,
                    "total": lot.total,
                    "state": "nodata",
                    "id": lot.id,
                    "lot_type": ltype,
                    "forecast": False
                })

    return {
        "last_updated": utc_now(),
        "lots": lots
    }
