import feedparser
from park_api.util import convert_date, generate_id
from park_api.geodata import GeoData

data_url = "http://www.pls-zh.ch/plsFeed/rss"
data_source = "https://www.stadt-zuerich.ch/portal/de/index/ogd/daten/parkleitsystem.html"

city_name = "Zürich"

total_number_map = {
    "Parkgarage am Central": 50,
    "Parkhaus Accu": 194,
    "Parkhaus Albisriederplatz": 66,
    "Parkhaus Bleicherweg": 275,
    "Parkhaus Center Eleven": 342,
    "Parkhaus City Parking": 620,
    "Parkhaus Cityport": 153,
    "Parkhaus Crowne Plaza": 520,
    "Parkhaus Dorflinde": 98,
    "Parkhaus Feldegg": 346,
    "Parkhaus Globus": 178,
    "Parkhaus Hardau II": 982,
    "Parkhaus Hauptbahnhof": 176,
    "Parkhaus Hohe Promenade": 556,
    "Parkhaus Jelmoli": 222,
    "Parkhaus Jungholz": 124,
    "Parkhaus Max-Bill-Platz": 59,
    "Parkhaus Messe Zürich AG": 2000,
    "Parkhaus Nordhaus": 175,
    "Parkhaus Octavo": 123,
    "Parkhaus Opéra": 299,
    "Parkhaus P West": 1000,
    "Parkhaus Park Hyatt": 267,
    "Parkhaus Parkside": 38,
    "Parkhaus Pfingstweid": 276,
    "Parkhaus Stampfenbach": 237,
    "Parkhaus Talgarten": 110,
    "Parkhaus USZ Nord": 90,
    "Parkhaus Uni Irchel": 1227,
    "Parkhaus Urania": 607,
    "Parkhaus Utoquai": 175,
    "Parkhaus Züri 11 Shopping": 60,
    "Parkhaus Zürichhorn": 245,
    "Parkplatz Bienen": 110,
    "Parkplatz Eisfeld": 240,
    "Parkplatz Theater 11": 188,
    "Parkplatz USZ Süd": 80
}

geodata = GeoData(__file__)

# Falls das hier jemals einer von den Menschen hinter OpenDataZürich lesen sollte: Ihr seid so toll <3

def parse_html(xml_data):
    feed = feedparser.parse(xml_data)

    last_updated = feed["entries"][0]["updated"]
    data = {
        "lots": [],
        # remove trailing timezone for consensistency
        "last_updated": last_updated.replace("Z", ""),
        "data_source": data_source
    }

    for entry in feed["entries"]:
        summary = parse_summary(entry["summary"])
        title = parse_title(entry["title"])

        old_id = entry["id"].split("=")[1]

        data["lots"].append({
            "name": title[0],
            "address": title[1],
            "id": generate_id(__file__, title[0]),
            "state": summary[0],
            "free": summary[1],
            "total": total_number_map.get(title[0], 0),
            "coords": geodata.coords(title[0]),
            "forecast": False,
        })

    return data


def parse_summary(summary):
    """Parse a string from the format 'open /   41' into both its params"""
    summary = summary.split("/")

    summary[0] = summary[0].strip()
    if "?" in summary[0]:
        summary[0] = "nodata"

    try:
        summary[1] = int(summary[1])
    except ValueError:
        summary[1] = 0
    return summary


def parse_title(title):
    """Parse a string from the format 'Parkgarage am Central / Seilergraben' into both its params"""
    title = title.split(" / ")
    return title
