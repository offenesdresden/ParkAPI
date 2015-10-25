from bs4 import BeautifulSoup
from park_api.util import convert_date
from park_api.geodata import GeoData

geodata = GeoData(__file__)


def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")

    # last update time (UTC)
    try:
        date_col = soup.select('p > strong')[-1].text
        update_time = convert_date(date_col, "Stand: %d.%m.%Y - %H:%M:%S")
    except ValueError:
        date_col = soup.select('p > strong')[-2].text
        update_time = convert_date(date_col, "Stand: %d.%m.%Y - %H:%M:%S")

    data = {
        "last_updated": update_time,
        "lots": []
    }

    # get all tables with lots
    raw_lot_list = soup.find_all("div", {"class": "listing"})

    # get all lots
    for lot_list in raw_lot_list:
        raw_lots = lot_list.select('tr + tr')

        for lot in raw_lots:
            lot_name = lot.select('a')[0].text

            try:
                lot_free = int(lot.select('td + td')[0].text)
            except ValueError:
                lot_free = 0

            try:
                if "green" in str(lot.select("td + td")[0]):
                    lot_state = "open"
                else:
                    lot_state = "closed"
            except ValueError:
                lot_state = "nodata"

            lot = geodata.lot(lot_name)
            data["lots"].append({
                "name": lot_name,
                "free": lot_free,
                "total": lot.total,
                "coords": lot.coords,
                "state": lot_state,
                "id": lot.id,
                "forecast": False
            })

    return data
