from bs4 import BeautifulSoup
from park_api.geodata import GeoData
from park_api.util import convert_date, generate_id

data_url = "http://www.ingolstadt.mobi/parkplatzauskunft.cfm"
data_source = "http://www.ingolstadt.mobi/parkplatzauskunft.cfm"
city_name = "Ingolstadt"

# Additional information for single lots: http://www2.ingolstadt.de/Wirtschaft/Parken/Parkeinrichtungen_der_IFG/

type_map = {
    "Theater-West": "Tiefgarage",
    "Theater-Ost": "Tiefgarage",
    "Schloss": "Tiefgarage",
    "Münster": "Tiefgarage",
    "Reduit Tilly": "Tiefgarage",
    "Hallenbad": "Parkplatz",
    "Festplatz": "Parkplatz",
    "Südl. Ringstraße": "Parkplatz",
    "Hauptbahnhof": "Parkhaus",
    "Nordbahnhof": "Parkplatz",
    "Hauptbahnhof Ost": "Parkhaus",
    "Congressgarage": "Tiefgarage"
}

total_number_map = {
    "Theater-West": 599,
    "Theater-Ost": 682,
    "Schloss": 435,
    "Münster": 384,
    "Reduit Tilly": 436,
    "Hallenbad": 836,
    "Festplatz": 1437,
    "Südl. Ringstraße": 257,
    "Hauptbahnhof": 812,
    "Nordbahnhof": 252,
    "Hauptbahnhof Ost": 240,
    "Congressgarage": 213
}

geodata = GeoData(__file__)

def parse_html(html):
    soup = BeautifulSoup(html)

    data = {
        "last_updated": convert_date(soup.p.string, "(%d.%m.%Y, %H.%M Uhr)"),
        "data_source": data_source,
        "lots": []
    }

    # get all lots
    raw_lots = soup.find_all("tr")

    for lot in raw_lots:
        elements = lot.find_all("td")

        lot_name = elements[0].text

        data["lots"].append({
            "name": lot_name,
            "free": int(elements[1].text),
            "total": total_number_map.get(lot_name, 0),
            "type": type_map.get(lot_name, "unbekannt"),
            "coords": geodata.coords(lot_name),
            "state": "nodata",
            "id": generate_id(__file__, lot_name),
            "forecast": False
        })

    return data
