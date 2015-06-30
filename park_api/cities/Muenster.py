from bs4 import BeautifulSoup
from park_api.util import convert_date, generate_id
from park_api.geodata import GeoData

data_url = "http://www5.stadt-muenster.de/parkhaeuser/"
data_source = "http://www.stadt-muenster.de"
city_name = "Münster"

total_number_map = {
    "PH Theater": 793,
    "PP Hörsterplatz": 202,
    "PH Alter Steinweg": 350,
    "Busparkplatz": 63,  # 63 (PKW) / 15 (Busse)
    "PP Schlossplatz Nord": 450,
    "PP Schlossplatz Süd": 460,
    "PH Aegidii": 780,
    "PP Georgskommende": 272,
    "PH Münster Arkaden": 248,
    "PH Karstadt": 183,
    "PH Stubengasse": 318,
    "PH Bremer Platz": 416,
    "PH Engelenschanze": 480,
    "PH Bahnhofstraße": 339,
    "PH Cineplex": 590,
    "PH Stadthaus 3": 372
}

state_map = {
    "frei": "open",
    "geschlossen": "closed",
    "besetzt": "open"
}

geodata = GeoData(__file__)

# Uncomment the following line if there's geodata in the format of Sample_City.geodata in this directory
# geodata = GeoData(city_name)

def parse_html(html):
    soup = BeautifulSoup(html)

    lot_table_trs = soup.select("table[cellpadding=5]")[0].find_all("tr")

    data = {
        "last_updated": convert_date(lot_table_trs[-1].text.strip(), "%d.%m.%Y %H:%M Uhr"),
        "data_source": data_source,
        "lots": []
    }

    for tr in lot_table_trs[1:-1]:
        tds = tr.find_all("td")
        type_and_name = process_name(tds[0].text)
        data["lots"].append({
            "name": type_and_name[1],
            "type": type_and_name[0],
            "free": int(tds[1].text),
            "total": total_number_map.get(tds[0].text, 0),
            "state": state_map.get(tds[2].text, ""),
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
        lot_name = name

    return lot_type, lot_name
