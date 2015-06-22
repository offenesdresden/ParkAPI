from bs4 import BeautifulSoup
import json
import datetime
import pytz

# The URL for the page where the parking lots are listed
data_url = "http://www.konstanz.de/tourismus/01759/01765/"

# Name of the city, just in case it contains umlauts which this filename shouldn't
city_name = "Konstanz"

# Name of this file (without '.py'), sorry for needing this, but it makes things easier
file_name = "Konstanz"


def parse_html(html):
    soup = BeautifulSoup(html)

    # last update time (UTC)
    update_time = soup.select('p > strong')[-1].text
    last_updated = datetime.datetime.strptime(update_time, "Stand: %d.%m.%Y - %H:%M:%S")
    local_timezone = pytz.timezone("Europe/Berlin")

    last_updated = local_timezone.localize(last_updated, is_dst=None)
    last_updated = last_updated.astimezone(pytz.utc).replace(tzinfo=None)

    data = {
        "last_updated": last_updated.replace(microsecond=0).isoformat(),
        "lots": []
    }

    # get all tables with lots
    raw_lot_list = soup.find_all("div", {"class": "listing"})

    # get all lots
    for lot_list in raw_lot_list:
        raw_lots = lot_list.select('tr + tr')

        for lot in raw_lots:
            lot_name = lot.select('a')[0].text
            lot_free = lot.select('td + td')[0].text
            data["lots"].append({
                "name": lot_name,
                "free": int(lot_free),
                "count": get_total_number(lot_name),
                "coords": get_geodata_for_lot(lot_name)
            })

    return data


def get_total_number(lot_name):
    mapping = {
        "Marktstätte": 268,
        "Altstadt": 359,
        "Lago": 930,
        "Augustiner / Karstadt": 284,
        "Fischmarkt": 158,
        "Döbele": 335,
        "Am Seerheim": 500,
        "Byk Gulden Str.": 100,
        "Benediktiner": 118,
        "Seerheincenter": 280
    }
    if lot_name not in mapping.keys():
        return 0
    else:
        return mapping[lot_name]


def get_geodata_for_lot(lot_name):
    geofile = open("./cities/" + file_name + ".geojson")
    geodata = geofile.read()
    geofile.close()
    geodata = json.loads(geodata)

    for feature in geodata["features"]:
        if feature["properties"]["name"] == lot_name:
            return {
                "lon": feature["geometry"]["coordinates"][0],
                "lat": feature["geometry"]["coordinates"][1]
            }
    return []


if __name__ == "__main__":
    file = open("../tests/konstanz.html")
    html_data = file.read()
    file.close()
    parse_html(html_data)
