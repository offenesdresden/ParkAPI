__author__ = 'kilian'

from bs4 import BeautifulSoup
import datetime

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
    date_last_changed = soup.find("ul", {"class": "links"}).findNext("p").text.strip()
    date_last_changed = datetime.datetime.strptime(date_last_changed, "%d.%m.%Y %H.%M Uhr")
    data["last_changed"] = str(date_last_changed)

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
    mapping = {
        "Altmarkt": {"lat": 51.05031, "lon": 13.73754},
        "An der Frauenkirche": {"lat": 51.05165, "lon": 13.7439},
        "Frauenkirche Neumarkt": {"lat": 51.05082, "lon": 13.74174},
        "Haus am Zwinger": {"lat": 51.05149, "lon": 13.73584},
        "Ostra - Allee": {"lat": 51.05383, "lon": 13.73093},
        "Schießgasse": {"lat": 51.05077, "lon": 13.7446},
        "Taschenbergpalais": {"lat": 51.05176, "lon": 13.7353},
        "Kongresszentrum": {"lat": 51.05922, "lon": 13.7305},
        "Parkhaus Mitte": {"lat": 51.05793, "lon": 13.72595},
        "Semperoper": {"lat": 51.05553, "lon": 13.73408},
        "World Trade Center": {"lat": 51.04952, "lon": 13.72215},
        "Altmarkt - Galerie": {"lat": 51.04951, "lon": 13.73407},
        "Centrum-Galerie": {"lat": 51.04547, "lon": 13.73368},
        "Ferdinandplatz": {"lat": 51.04645, "lon": 13.73988},
        "Karstadt": {"lat": 51.04669, "lon": 13.73801},
        "Reitbahnstraße": {"lat": 51.04334, "lon": 13.73279},
        "Wiener Platz/Hbf.": {"lat": 51.04187, "lon": 13.73155},
        "Wöhrl - Florentinum": {"lat": 51.04449, "lon": 13.73772},
        "City  Center": {"lat": 51.03855, "lon": 13.73151},
        "Blüherstraße": {"lat": 51.04413, "lon": 13.74859},
        "Lindengasse": {"lat": 51.04151, "lon": 13.74126},
        "Lingnerallee": {"lat": 51.04379, "lon": 13.75035},
        "Pirnaische Straße": {"lat": 51.04641, "lon": 13.74746},
        "Pirnaischer Platz": {"lat": 51.04785, "lon": 13.74326},
        "Terrassenufer": {"lat": 51.05357, "lon": 13.74688},
        "Zinzendorfstraße": {"lat": 51.04458, "lon": 13.74466},
        "Bahnhof Neustadt": {"lat": 51.06541, "lon": 13.74196},
        "Hauptstraße": {"lat": 51.06057, "lon": 13.7449},
        "Palaisplatz": {"lat": 51.06026, "lon": 13.73924},
        "Sarrasanistraße": {"lat": 51.05776, "lon": 13.74493},
        "Theresienstraße": {"lat": 51.06314, "lon": 13.74208},
        "Wiesentorstraße": {"lat": 51.05706, "lon": 13.74339},
        "Wigardstraße": {"lat": 51.05768, "lon": 13.75072},
        "Flutrinne": {"lat": 51.06752, "lon": 13.71951},
        "Messegelände": {"lat": 51.06911, "lon": 13.71218},
        "Bühlau": {"lat": 51.06065, "lon": 13.85426},
        "Cossebaude": {"lat": 51.08521, "lon": 13.63258},
        "Kaditz": {"lat": 51.08133, "lon": 13.69097},
        "Langebrück": {"lat": 51.12714, "lon": 13.84038},
        "Pennrich": {"lat": 51.0405, "lon": 13.62639},
        "Prohlis": {"lat": 50.99958, "lon": 13.79952},
        "Terrassenufer Bus": {"lat": 51.05229, "lon": 13.75051}
    }
    if lot_name not in mapping.keys():
        return []
    return mapping[lot_name]
