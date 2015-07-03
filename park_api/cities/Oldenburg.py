from bs4 import BeautifulSoup
from park_api.util import convert_date, generate_id
from park_api.geodata import GeoData

# URL for the page where the scraper can gather the data
data_url = "http://oldenburg-service.de/pls2.php"

# URL that is displayed as the source of this data, usually the base domain of the URL above
data_source = "http://www.oldenburg.de/microsites/verkehr/parken/parkplaetzeparkleitsystem/parkplaetze.html"

# Name of the city, just in case it contains umlauts, spaces or other things which this filename shouldn't
city_name = "Oldenburg"

# This loads the geodata for this city if <city>.geojson exists in the same directory as this file.
# No need to remove this if there's no geodata (yet), everything will still work.
geodata = GeoData(__file__)

# This function is called by the scraper and given the data of the page specified as data_url above.
# It's supposed to return a dictionary containing everything the current spec expects. Tests will fail if it doesn't ;)
def parse_html(html):
    # BeautifulSoup is a great and easy way to parse the html and find the bits and pieces we're looking for.
    soup = BeautifulSoup(html)

    # last_updated is the date when the data on the page was last updated
    last_updated = str(soup.select("body"))
    start = str.find(last_updated, "Letzte Aktualisierung:") + 23
    last_updated = last_updated[start:start + 16] + ' Uhr'

    data = {
        # convert_date is a utility function you can use to turn this date into the correct string format
        "last_updated": convert_date(last_updated, "%d.%m.%Y %H:%M Uhr"),
        "data_source": data_source,
        "lots": []
    }

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
        # CCO 1 & 2 are together only known together with 420, but they seem to be somewhat like this
        "CCO Parkdeck 1": [190, "Heiligengeiststraße 4"],
        "CCO Parkdeck 2": [230, "Heiligengeiststraße 4"],
        "Hbf/ZOB": [358, "Karlstraße"],
        "Theaterwall": [125, "Theaterwall 4"],
        "Theatergarage": [107, "Roonstraße"],
        "Heiligengeist-Höfe": [275, "Georgstraße"],
        "Schlosshöfe": [430, "Mühlenstraße"],
    }

    for tr in soup.find_all("tr"):
        if tr.td is None:
            continue
        td = tr.findAll('td')
        lot_name = td[0].b.string
        lot_free = int(td[1].b.text)

        # get the values from the map above, or return zero
        # should trown an execption -> error@parkenDD.de 
        lot_total = lots_map[lot_name][0]
        lot_address = lots_map[lot_name][1]

        # lot_type = tr.find("td").text

        # please be careful about the state only being allowed to contain either open, closed or nodata
        # should the page list other states, please map these into the three listed possibilities
        state = status_map.get(td[3].text, "nodata")

        data["lots"].append({
            # use the utility function generate_id to generate an ID for this lot
            # it takes this file path and the lot's name as params
            "id": generate_id(__file__, lot_name),
            "name": lot_name,
            "free": lot_free,
            "state": state,
            "total": lot_total,
            "address": lot_address,
            "coords": geodata.coords(lot_name),
            # "type": lot_type,
            "forecast": False
        })
    return data
