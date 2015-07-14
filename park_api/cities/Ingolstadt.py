from bs4 import BeautifulSoup
from park_api.geodata import GeoData
from park_api.util import convert_date, generate_id

data_url = "http://www.ingolstadt.mobi/parkplatzauskunft.cfm"
data_source = "http://www.ingolstadt.mobi/parkplatzauskunft.cfm"
city_name = "Ingolstadt"

# Additional information for single lots: http://www2.ingolstadt.de/Wirtschaft/Parken/Parkeinrichtungen_der_IFG/

data_map = {
    "Theater-West": {
        "type": "Tiefgarage",
        "total": 599,
        "address": "Schutterstraße"
    },
    "Theater-Ost": {
        "type": "Tiefgarage",
        "total": 682,
        "address": "Schloßländle"
    },
    "Schloss": {
        "type": "Tiefgarage",
        "total": 435,
        "address": "Esplanade"
    },
    "Münster": {
        "type": "Tiefgarage",
        "total": 384,
        "address": "Bergbräustraße"
    },
    "Reduit Tilly": {
        "type": "Tiefgarage",
        "total": 436,
        "address": "Regimentstraße"
    },
    "Hallenbad": {
        "type": "Parkplatz",
        "total": 836,
        "address": "Jahnstraße 9"
    },
    "Festplatz": {
        "type": "Parkplatz",
        "total": 1437,
        "address": "Dreizehnerstraße"
    },
    "Südl. Ringstraße": {
        "type": "Parkplatz",
        "total": 257,
        "address": "Südliche Ringstraße"
    },
    "Hauptbahnhof": {
        "type": "Parkhaus",
        "total": 812,
        "address": "Elisabethstraße 3"
    },
    "Nordbahnhof": {
        "type": "Parkplatz",
        "total": 252,
        "address": "Am Nordbahnhof 3"
    },
    "Hauptbahnhof Ost": {
        "type": "Parkhaus",
        "total": 240,
        "address": "Martin-Hemm-Straße 8"
    },
    "Congressgarage": {
        "type": "Tiefgarage",
        "total": 213,
        "address": "Schloßlände 25"
    }
}

geodata = GeoData(__file__)

def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")

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
            "total": data_map.get(lot_name)["total"],
            "type": data_map.get(lot_name)["type"],
            "address": data_map.get(lot_name)["address"],
            "coords": geodata.coords(lot_name),
            "state": "nodata",
            "id": generate_id(__file__, lot_name),
            "forecast": False
        })

    return data
