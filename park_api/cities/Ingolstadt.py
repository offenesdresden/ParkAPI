from bs4 import BeautifulSoup
from park_api.models import GeoData, Lots
from park_api.util import parse_date

# Additional information for single lots:
# http://www2.ingolstadt.de/Wirtschaft/Parken/Parkeinrichtungen_der_IFG/
geodata = GeoData(__file__)


def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")

    updated_at = parse_date(soup.p.string, "(%d.%m.%Y, %H.%M Uhr)")
    lots = Lots()

    for raw_lot in soup.find_all("tr"):
        tds = raw_lot.find_all("td")

        if "class" in raw_lot.attrs and raw_lot["class"][0] == "strike":
            state = "closed"
        else:
            state = "open"

        lot = geodata.lot(tds[0].text)
        lot.free = int(tds[1].text)
        lot.state = state
        lot.updated_at = updated_at
        lots.append(lot)
    return lots
