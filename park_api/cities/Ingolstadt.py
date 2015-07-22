from bs4 import BeautifulSoup
from park_api.geodata import GeoData
from park_api.util import convert_date

data_url = "http://www.ingolstadt.mobi/parkplatzauskunft.cfm"
data_source = "http://www.ingolstadt.mobi/parkplatzauskunft.cfm"
city_name = "Ingolstadt"

# Additional information for single lots: http://www2.ingolstadt.de/Wirtschaft/Parken/Parkeinrichtungen_der_IFG/

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

    for raw_lot in raw_lots:
        elements = raw_lot.find_all("td")

        lot_name = elements[0].text

        lot = geodata.lot(lot_name)
        data["lots"].append({
            "name": lot.name,
            "free": int(elements[1].text),
            "total": lot.total,
            "type": lot.type,
            "address": lot.address,
            "coords": lot.coords,
            "state": "nodata",
            "id": lot.id,
            "forecast": False
        })

    return data
