__author__ = 'kilian'

import requests
from bs4 import BeautifulSoup

dataURL = "http://www.dresden.de/freie-parkplaetze/"

def _get_html():
    headers = {
        "User-Agent": "ParkAPI v0.1 - Info: https://github.com/kiliankoe/ParkAPI"
    }

    r = requests.get(dataURL, headers=headers)
    return r.text

def _parse_html():
    soup = BeautifulSoup(_get_html())
    data = []

    # Die einzelnen Stadteile sind in einzelne tables gegliedert
    section_tables = soup.find_all("tbody")
    for table in section_tables:

        # jeder parkplatz steckt in einer eigenen row
        rows = table.find_all("tr")
        for row in rows:

            raw_lot_data = row.find_all("td")

            name = raw_lot_data[0].find("a").text

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

            data.append({
                "name": name,
                "coords": coords,
                "state": state,
                "free": free,
                "count": count
            })
    return data

def get_data():
    return _parse_html()
    # return {"foo": "bar"}

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
        "Altmarkt": [51.05031, 13.73754],
        "An der Frauenkirche": [51.05165, 13.7439],
        "Frauenkirche Neumarkt": [51.05082, 13.74174],
        "Haus am Zwinger": [51.05149, 13.73584],
        "Ostra - Allee": [51.05383, 13.73093],
        "Schießgasse": [51.05077, 13.7446],
        "Taschenbergpalais": [51.05176, 13.7353],
        "Kongresszentrum": [51.05922, 13.7305],
        "Parkhaus Mitte": [51.05793, 13.72595],
        "Semperoper": [51.05553, 13.73408],
        "World Trade Center": [51.04952, 13.72215],
        "Altmarkt - Galerie": [51.04951, 13.73407],
        "Centrum-Galerie": [51.04547, 13.73368],
        "Ferdinandplatz": [51.04645, 13.73988],
        "Karstadt": [51.04669, 13.73801],
        "Reitbahnstraße": [51.04334, 13.73279],
        "Wiener Platz/Hbf.": [51.04187, 13.73155],
        "Wöhrl - Florentinum": [51.04449, 13.73772],
        "City  Center": [51.03855, 13.73151],
        "Blüherstraße": [51.04413, 13.74859],
        "Lindengasse": [51.04151, 13.74126],
        "Lingnerallee": [51.04379, 13.75035],
        "Pirnaische Straße": [51.04641, 13.74746],
        "Pirnaischer Platz": [51.04785, 13.74326],
        "Terrassenufer": [51.05357, 13.74688],
        "Zinzendorfstraße": [51.04458, 13.74466],
        "Bahnhof Neustadt": [51.06541, 13.74196],
        "Hauptstraße": [51.06057, 13.7449],
        "Palaisplatz": [51.06026, 13.73924],
        "Sarrasanistraße": [51.05776, 13.74493],
        "Theresienstraße": [51.06314, 13.74208],
        "Wiesentorstraße": [51.05706, 13.74339],
        "Wigardstraße": [51.05768, 13.75072],
        "Flutrinne": [51.06752, 13.71951],
        "Messegelände": [51.06911, 13.71218],
        "Bühlau": [51.06065, 13.85426],
        "Cossebaude": [51.08521, 13.63258],
        "Kaditz": [51.08133, 13.69097],
        "Langebrück": [51.12714, 13.84038],
        "Pennrich": [51.0405, 13.62639],
        "Prohlis": [50.99958, 13.79952],
        "Terrassenufer Bus": [51.05229, 13.75051]
    }
    if lot_name not in mapping.keys():
        return []
    return mapping[lot_name]
