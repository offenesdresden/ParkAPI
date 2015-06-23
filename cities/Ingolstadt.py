from bs4 import BeautifulSoup
import datetime
import pytz
from geodata import GeoData

data_url = "http://www.ingolstadt.mobi/parkplatzauskunft.cfm"
city_name = "Ingolstadt"
file_name = "Ingolstadt"

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

geodata = GeoData(city_name)

# Additional information for single lots: http://www2.ingolstadt.de/Wirtschaft/Parken/Parkeinrichtungen_der_IFG/

def parse_html(html):
    soup = BeautifulSoup(html)

    # get time last updated
    last_updated = datetime.datetime.strptime(soup.p.string, "(%d.%m.%Y, %H.%M Uhr)")
    local_timezone = pytz.timezone("Europe/Berlin")

    last_updated = local_timezone.localize(last_updated, is_dst=None)
    last_updated = last_updated.astimezone(pytz.utc).replace(tzinfo=None)

    data = {
        "last_updated": last_updated.replace(microsecond=0).isoformat(),
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
            "count": total_number_map.get(lot_name, 0),
            "type": type_map.get(lot_name, "unbekannt"),
            "coords": geodata.coords(lot_name)
        })

    return data
