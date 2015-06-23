from bs4 import BeautifulSoup
import datetime
import pytz
from geodata import GeoData

data_url = "http://www.dresden.de/freie-parkplaetze"
city_name = "Dresden"
file_name = "Dresden"
detail_url = "/parken/detail"

status_image_map = {
        "/img/parken/p_gruen.gif": "many",
        "/img/parken/p_gelb.gif": "few",
        "/img/parken/p_rot.gif": "full",
        "/img/parken/p_geschlossen.gif": "closed",
        "/img/parken/p_blau.gif": "nodata"
}

geodata = GeoData(city_name)

def parse_html(html):
    soup = BeautifulSoup(html)
    data = {
        "lots": []
    }

    # Letzte Aktualisierung auslesen, ich liebe html parsing m(
    last_updated = soup.find("ul", {"class": "links"}).findNext("p").text.strip()
    last_updated = datetime.datetime.strptime(last_updated, "%d.%m.%Y %H.%M Uhr")
    local_timezone = pytz.timezone("Europe/Berlin")

    last_updated = local_timezone.localize(last_updated, is_dst=None)
    last_updated = last_updated.astimezone(pytz.utc).replace(tzinfo=None)

    data["last_updated"] = last_updated.replace(microsecond=0).isoformat()

    # Die einzelnen Stadteile sind in einzelne tables gegliedert
    section_tables = soup.find_all("tbody")
    for table in section_tables:

        # jeder parkplatz steckt in einer eigenen row
        rows = table.find_all("tr")
        for row in rows:

            raw_lot_data = row.find_all("td")

            name = raw_lot_data[0].find("a").text

            id = raw_lot_data[0].find("a")["href"][-4:]

            state = status_image_map.get(raw_lot_data[0].find("img")["src"], "nodata")

            coords = geodata.coords(name)

            count = raw_lot_data[1].text
            count = count.strip()
            if count is "":
                count = 0
            count = int(count)

            free = raw_lot_data[2].text
            free = free.strip()
            if free is "":
                free = 0
            free = int(free)

            data["lots"].append({
                "name": name,
                "coords": coords,
                "id": id,
                "state": state,
                "free": free,
                "count": count
            })
    return data


# def get_lot_details(lot_id):
#     params = {
#         "id": lot_id
#     }
#     r = requests.get(data_url + detail_url, params=params)
#     return r.text
