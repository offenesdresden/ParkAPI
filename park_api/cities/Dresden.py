from bs4 import BeautifulSoup
from park_api.models import GeoData, Lots
from park_api.util import parse_date

geodata = GeoData(__file__)


def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    date = soup.find(id="P1_LAST_UPDATE").text

    lots = Lots()
    updated_at = parse_date(date, "%d.%m.%Y %H:%M:%S")
    for table in soup.find_all("table"):
        if table["summary"] == "":
            continue
        region = table["summary"]

        for lot_row in table.find_all("tr"):
            if lot_row.find("th") is not None:
                continue

            name = lot_row.find("td", {"headers": "BEZEICHNUNG"}).text
            lot = geodata.lot(name)

            col = lot_row.find("td", {"headers": "FREI"})
            if col.text.strip() == "":
                lot.free = 0
            else:
                lot.free = int(col.text)

            cls = lot_row.find("div")["class"]
            if "green" in cls or "yellow" in cls or "red" in cls:
                lot.state = "open"
            elif "park-closed" in cls:
                lot.state = "closed"

            col = lot_row.find("td", {"headers": "KAPAZITAET"})
            try:
                lot.total = int(col.text)
            except ValueError:
                pass
            lot.region = region
            lot.updated_at = updated_at
            lots.append(lot)
    return lots
