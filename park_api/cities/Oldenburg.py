from bs4 import BeautifulSoup
from park_api.util import parse_date
from park_api.models import GeoData, Lots

geodata = GeoData(__file__)

status_map = {
    "Offen": "open",
    "Geschlossen": "closed"
}

# Oldenburg does not send the totals on there website,
# so wie take some Values from a 2011st PDF:
# http://www.oldenburg.de/fileadmin/oldenburg/Benutzer/PDF/41/414/Parkplatz_Uebersicht2.pdf
# and http://gis4oldenburg.oldenburg.de/?es=C12S77
# what possible can go wrong ¯\_(ツ)_/¯
lots_map = {
    "Waffenplatz": [650, "Waffenplatz 3"],
    "City": [440, "Staulinie 10"],
    "Galeria Kaufhof": [326, "Ritterstraße"],
    "Pferdemarkt": [401, "Pferdemarkt 13"],
    # CCO 1 & 2 are together only known together with 420,
    # but they seem to be somewhat like this
    "CCO Parkdeck 1": [190, "Heiligengeiststraße 4"],
    "CCO Parkdeck 2": [230, "Heiligengeiststraße 4"],
    "Hbf/ZOB": [358, "Karlstraße"],
    "Theaterwall": [125, "Theaterwall 4"],
    "Theatergarage": [107, "Roonstraße"],
    "Heiligengeist-Höfe": [275, "Georgstraße"],
    "Schlosshöfe": [430, "Mühlenstraße"],
}


def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")

    last_updated = str(soup.select("body"))
    start = str.find(last_updated, "Letzte Aktualisierung:") + 23
    last_updated = last_updated[start:start + 16] + ' Uhr'

    lots = Lots()
    updated_at = parse_date(last_updated, "%d.%m.%Y %H:%M Uhr")
    for tr in soup.find_all("tr"):
        if tr.td is None:
            continue
        td = tr.findAll('td')
        name = td[0].b.string
        lot = geodata.lot(name)
        lot.free = int(td[1].b.text)
        lot.updated_at = updated_at

        # get the values from the map above, or return zero
        # should trown an execption -> error@parkenDD.de
        lot.total = lots_map[name][0]
        lot.address = lots_map[name][1]

        # please be careful about the state only being allowed to contain
        # either open, closed or nodata should the page list other states,
        # please map these into the three listed possibilities
        lot.state = status_map.get(td[3].text, "nodata")

        lots.append(lot)
    return lots
