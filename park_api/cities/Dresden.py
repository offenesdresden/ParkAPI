import os
from bs4 import BeautifulSoup
from park_api.geodata import GeoData
from park_api.util import convert_date, get_most_lots_from_known_data

data_url = "https://apps.dresden.de/ords/f?p=1110"
data_source = "https://www.dresden.de/parken"
city_name = "Dresden"
lat = 51.0508900
lon = 13.7383200

geodata = GeoData(__file__)


def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    date_field = soup.find(id="P1_LAST_UPDATE").text
    last_updated = convert_date(date_field, "%d.%m.%Y %H:%M:%S")
    data = {
        "lots": [],
        "data_source": data_source,
        "last_updated": last_updated
    }

    for table in soup.find_all("table"):
        if table["summary"] != "":
            region = table["summary"]

            for lot_row in table.find_all("tr"):
                if lot_row.find("th") is not None:
                    continue

                cls = lot_row.find("div")["class"]
                state = "nodata"
                if "green" in cls or "yellow" in cls or "red" in cls:
                    state = "open"
                elif "park-closed" in cls:
                    state = "closed"

                lot_name = lot_row.find("td", {"headers": "BEZEICHNUNG"}).text


                try:
                    free = int(lot_row.find("td", {"headers": "FREI"}).text)
                except ValueError:
                    free = 0

                try:
                    total = int(lot_row.find("td", {"headers": "KAPAZITAET"}).text)
                except ValueError:
                    total = get_most_lots_from_known_data("Dresden", lot_name)

                lot = geodata.lot(lot_name)
                forecast = os.path.isfile("forecast_data/" + lot.id + ".csv")

                data["lots"].append({
                    "coords": lot.coords,
                    "name": lot_name,
                    "total": total,
                    "free": free,
                    "state": state,
                    "id": lot.id,
                    "lot_type": lot.type,
                    "address": lot.address,
                    "forecast": forecast,
                    "region": region
                })

    return data
