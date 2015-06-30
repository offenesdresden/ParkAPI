from bs4 import BeautifulSoup
from park_api.geodata import GeoData
from park_api.util import convert_date, generate_id

data_url = "http://www.dresden.de/freie-parkplaetze"
data_source = "http://www.dresden.de"
city_name = "Dresden"
detail_url = "/parken/detail"

status_image_map = {
    "/img/parken/p_gruen.gif": "open",
    "/img/parken/p_gelb.gif": "open",
    "/img/parken/p_rot.gif": "open",
    "/img/parken/p_geschlossen.gif": "closed",
    "/img/parken/p_blau.gif": "nodata"
}

type_map = {
    "Altmarkt": "Tiefgarage",
    "An der Frauenkirche": "Tiefgarage",
    "Frauenkirche Neumarkt": "Tiefgarage",
    "Haus am Zwinger": "Tiefgarage",
    "Ostra - Allee": "Parkplatz",
    "Schießgasse": "Parkplatz",
    "Taschenbergpalais": "Tiefgarage",
    "Kongresszentrum": "Tiefgarage",
    "Parkhaus Mitte": "Parkhaus",
    "Semperoper": "Tiefgarage",
    "World Trade Center": "Tiefgarage",
    "Altmarkt - Galerie": "Tiefgarage",
    "Centrum-Galerie": "Parkhaus",
    "Ferdinandplatz": "Parkplatz",
    "Karstadt": "Tiefgarage",
    "Reitbahnstraße": "Parkplatz",
    "Wiener Platz/Hbf.": "Tiefgarage",
    "Wöhrl - Florentinum": "Tiefgarage",
    "City Center": "Tiefgarage",
    "Blüherstraße": "Parkplatz",
    "Lindengasse": "Parkplatz",
    "Lingnerallee": "Parkplatz",
    "Pirnaische Straße": "Parkplatz",
    "Pirnaischer Platz": "Parkplatz",
    "Terrassenufer": "Parkplatz",
    "Zinzendorfstraße": "Parkplatz",
    "Bahnhof Neustadt": "Parkplatz",
    "Hauptstraße": "Parkhaus",
    "Palaisplatz": "Parkplatz",
    "Sarrasanistraße": "Parkplatz",
    "Theresienstraße": "Parkplatz",
    "Wiesentorstraße": "Parkplatz",
    "Wigardstraße": "Parkplatz",
    "Flutrinne": "Parkplatz",
    "Messegelände": "Parkplatz",
    "Bühlau": "Parkplatz",
    "Cossebaude": "",
    "Gompitz": "",
    "Kaditz": "",
    "Klotzsche": "",
    "Langebrück": "",
    "Pennrich": "",
    "Prohlis": "",
    "Reick": "",
    "Terrassenufer Bus": ""
}

address_map = {
    "Altmarkt": "Wilsdruffer Straße",
    "An der Frauenkirche": "An der Frauenkirche 12a",
    "Frauenkirche Neumarkt": "Landhausstraße 2",
    "Haus am Zwinger": "Kleine Brüdergasse 3",
    "Ostra - Allee": "Ostra-Allee",
    "Schießgasse": "Schießgasse",
    "Taschenbergpalais": "Kleine Brüdergasse",
    "Kongresszentrum": "Ostra-Ufer 2",
    "Parkhaus Mitte": "Magdeburger Str. 1",
    "Semperoper": "Devrientstraße",
    "World Trade Center": "Ammonstraße 70",
    "Altmarkt - Galerie": "Webergasse 1",
    "Centrum-Galerie": "Reitbahnstraße",
    "Ferdinandplatz": "Ferdinandplatz",
    "Karstadt": "Prager Straße 12",
    "Reitbahnstraße": "Reitbahnstraße",
    "Wiener Platz/Hbf.": "Wiener Platz",
    "Wöhrl - Florentinum": "Prager Straße 8 - 10",
    "City Center": "Friedrich-List-Platz 2",
    "Blüherstraße": "Blüherstraße",
    "Lindengasse": "Lindengasse",
    "Lingnerallee": "Lingnerallee",
    "Pirnaische Straße": "Pirnaische Straße",
    "Pirnaischer Platz": "Pirnaischer Platz",
    "Terrassenufer": "Terrassenufer",
    "Zinzendorfstraße": "Zinzendorfstraße",
    "Bahnhof Neustadt": "Schlesischer Platz",
    "Hauptstraße": "Metzer Straße",
    "Palaisplatz": "Palaisplatz",
    "Sarrasanistraße": "Sarrasanistraße",
    "Theresienstraße": "Theresienstraße 15",
    "Wiesentorstraße": "Wiesentorstraße",
    "Wigardstraße": "Wigardstraße",
    "Flutrinne": "Messering",
    "Messegelände": "Messering 6",
    "Bühlau": "Quohrener Straße",
    "Cossebaude": "Bahnhofstraße Cossebaude",
    "Gompitz": "",
    "Kaditz": "Kötschenbroder Str.",
    "Klotzsche": "",
    "Langebrück": "Güterbahnhofstraße Langebrück",
    "Pennrich": "Oskar-Maune-Straße",
    "Prohlis": "Langer Weg",
    "Reick": "",
    "Terrassenufer Bus": "Terrassenufer"
}

geodata = GeoData(__file__)


def parse_html(html):
    soup = BeautifulSoup(html)
    data = {
        "lots": [],
        "data_source": data_source
    }

    # Letzte Aktualisierung auslesen, ich liebe html parsing m(
    last_updated = soup.find("ul", {"class": "links"}).findNext("p").text.strip()

    data["last_updated"] = convert_date(last_updated, "%d.%m.%Y %H.%M Uhr")

    section_tables = soup.find_all("table", {"class": "zahlen"})
    for table in section_tables:
        region = table.select("thead th")[0].text

        for row in table.select("tbody tr"):
            raw_lot_data = row.find_all("td")

            name = raw_lot_data[0].find("a").text

            lot_id = raw_lot_data[0].find("a")["href"][-4:]

            state = status_image_map.get(raw_lot_data[0].find("img")["src"], "nodata")

            coords = geodata.coords(name)

            total = raw_lot_data[1].text
            total = total.strip()
            if total == "":
                total = 0
            total = int(total)

            free = raw_lot_data[2].text
            free = free.strip()
            if free == "":
                free = 0
            free = int(free)

            data["lots"].append({
                "coords": coords,
                "name": name,
                "total": total,
                "free": free,
                "state": state,
                "id": generate_id(__file__, name),
                "lot_type": type_map.get(name, ""),
                "address": address_map.get(name, ""),
                "forecast": False,
                "region": region
            })

    return data
