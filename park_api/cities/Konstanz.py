from bs4 import BeautifulSoup
from park_api.util import parse_date
from park_api.models import GeoData, Lots

geodata = GeoData(__file__)


def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")

    # last update time (UTC)
    try:
        date_col = soup.select('p > strong')[-1].text
        updated_at = parse_date(date_col, "Stand: %d.%m.%Y - %H:%M:%S")
    except ValueError:
        date_col = soup.select('p > strong')[-2].text
        updated_at = parse_date(date_col, "Stand: %d.%m.%Y - %H:%M:%S")

    lots = Lots()
    for lot_list in soup.find_all("div", {"class": "listing"}):
        raw_lots = lot_list.select('tr + tr')

        for raw_lot in raw_lots:
            name = raw_lot.select('a')[0].text
            lot = geodata.lot(name)
            lot.updated_at = updated_at
            lot.free = int(raw_lot.select('td + td')[0].text)

            if "green" in str(raw_lot.select("td + td")[0]):
                lot.state = "open"
            else:
                lot.state = "closed"

            lots.append(lot)
    return lots
