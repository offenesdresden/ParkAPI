from bs4 import BeautifulSoup
from park_api.geodata import GeoData
from park_api.util import convert_date

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
    
    for row in soup.find_all("div", class_='vc_row wpb_row section vc_row-fluid parking-lots grid_section'):
      for column in row.find_all("div", class_='vc_col-sm-3 wpb_column vc_column_container '):
        h3 = column.find_all("h3")
        if not h3[0].a == None:
          name = h3[0].a.string
          lot = geodata.lot(name)
          lots.append({
            "name": name,
            "coords": lot.coords,
            "free": int(h3[1].span.strong.get_text()),
            "address": lot.address,
            "total": lot.total,
            "state": "nodata",
            "id": lot.id,
            "forecast": False
         })
    
    return {
        "last_updated": "",
        "lots": lots
    }
