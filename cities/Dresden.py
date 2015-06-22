from bs4 import BeautifulSoup
import datetime
import json

data_url = "http://www.dresden.de/freie-parkplaetze"
city_name = "Dresden"
file_name = "Dresden"
detail_url = "/parken/detail"


def parse_html(html):
    soup = BeautifulSoup(html)
    data = {
        "lots": []
    }

    # Letzte Aktualisierung auslesen, ich liebe html parsing m(
    last_updated = soup.find("ul", {"class": "links"}).findNext("p").text.strip()
    last_updated = datetime.datetime.strptime(last_updated, "%d.%m.%Y %H.%M Uhr")
    data["last_updated"] =  datetime.datetime.utcfromtimestamp(last_updated.timestamp()).replace(microsecond=0).isoformat()

    # Die einzelnen Stadteile sind in einzelne tables gegliedert
    section_tables = soup.find_all("tbody")
    for table in section_tables:

        # jeder parkplatz steckt in einer eigenen row
        rows = table.find_all("tr")
        for row in rows:

            raw_lot_data = row.find_all("td")

            name = raw_lot_data[0].find("a").text

            id = raw_lot_data[0].find("a")["href"][-4:]

            state = get_status_by_image(raw_lot_data[0].find("img")["src"])

            coords = get_geodata_for_lot(name)

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

def get_status_by_image(image_name):
    mapping = {
        "/img/parken/p_gruen.gif": "many",
        "/img/parken/p_gelb.gif": "few",
        "/img/parken/p_rot.gif": "full",
        "/img/parken/p_geschlossen.gif": "closed",
        "/img/parken/p_blau.gif": "nodata"
    }
    if image_name not in mapping.keys():
        return "nodata"
    return mapping[image_name]


def get_geodata_for_lot(lot_name):
    geofile = open("./cities/Dresden.geojson")
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
    file = open("../tests/dresden.html")
    html_data = file.read()
    file.close()
    print(parse_html(html_data))
