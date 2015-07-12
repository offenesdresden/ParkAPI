from bs4 import BeautifulSoup
from park_api.geodata import GeoData
from park_api.util import convert_date, generate_id, get_most_lots_from_known_data
import os.path

data_url = "https://apps.dresden.de/ords/f?p=1110"
data_source = "https://www.dresden.de/parken"
city_name = "Dresden"

type_map = {
    "Altmarkt": "Tiefgarage",
    "An der Frauenkirche": "Tiefgarage",
    "Frauenkirche Neumarkt": "Tiefgarage",
    "Haus am Zwinger": "Tiefgarage",
    "Ostra-Allee": "Parkplatz",
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
    "Cossebaude": "Parkplatz",
    "Gompitz": "Parkplatz",
    "Kaditz": "Parkplatz",
    "Klotzsche": "Parkplatz",
    "Langebrück": "Parkplatz",
    "Pennrich": "Parkplatz",
    "Prohlis": "Parkplatz",
    "Reick": "Parkplatz",
    "Terrassenufer Bus": "Parkplatz"
}

address_map = {
    "Altmarkt": "Wilsdruffer Straße",
    "An der Frauenkirche": "An der Frauenkirche 12a",
    "Frauenkirche Neumarkt": "Landhausstraße 2",
    "Haus am Zwinger": "Kleine Brüdergasse 3",
    "Ostra-Allee": "Ostra-Allee",
    "Schießgasse": "Schießgasse",
    "Taschenbergpalais": "Kleine Brüdergasse",
    "Kongresszentrum": "Ostra-Ufer 2",
    "Parkhaus Mitte": "Magdeburger Str. 1",
    "Semperoper": "Devrientstraße",
    "World Trade Center": "Ammonstraße 70",
    "Altmarkt - Galerie": "Webergasse 1",
    "Centrum-Galerie": "Reitbahnstraße",
    "Centrum Galerie": "Reitbahnstraße",
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
    "Gompitz": "Gompitzer Höhe",
    "Kaditz": "Kötschenbroder Str.",
    "Klotzsche": "Zur Neuen Brücke",
    "Langebrück": "Güterbahnhofstraße Langebrück",
    "Pennrich": "Oskar-Maune-Straße",
    "Prohlis": "Langer Weg",
    "Reick": "Lohrmannstraße",
    "Terrassenufer Bus": "Terrassenufer"
}

geodata = GeoData(__file__)


def parse_html(html):
    soup = BeautifulSoup(html)
    data = {
        "lots": [],
        "data_source": data_source,
        "last_updated": convert_date(soup.find(id="P1_LAST_UPDATE").text, "%d.%m.%Y %H:%M:%S")
    }

    for table in soup.find_all("table"):
        if table["summary"] != "":
            region = table["summary"]

            for lot_row in table.find_all("tr"):
                if lot_row.find("th") is not None:
                    continue

                state_div = lot_row.find("div")
                if "green" in state_div["class"]:
                    state = "open"
                elif "yellow" in state_div["class"]:
                    state = "open"
                elif "red" in state_div["class"]:
                    state = "open"
                elif "park-closed" in state_div["class"]:
                    state = "closed"
                else:
                    state = "nodata"

                lot_name = lot_row.find("td", {"headers": "BEZEICHNUNG"}).text

                try:
                    free = int(lot_row.find("td", {"headers": "FREI"}).text)
                except ValueError:
                    free = 0

                try:
                    total = int(lot_row.find("td", {"headers": "KAPAZITAET"}).text)
                except ValueError:
                    total = get_most_lots_from_known_data("Dresden", lot_name)

                id = generate_id(__file__, lot_name)
                forecast = os.path.isfile("forecast_data/" + id + ".csv")

                data["lots"].append({
                    "coords": geodata.coords(lot_name),
                    "name": lot_name,
                    "total": total,
                    "free": free,
                    "state": state,
                    "id": id,
                    "lot_type": type_map.get(lot_name, ""),
                    "address": address_map.get(lot_name, ""),
                    "forecast": forecast,
                    "region": region
                })

    return data
