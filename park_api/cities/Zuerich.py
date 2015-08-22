import feedparser
from park_api.util import convert_date
from park_api.geodata import GeoData

data_url = "http://www.pls-zh.ch/plsFeed/rss"
data_source = "https://www.stadt-zuerich.ch/portal/de/index/ogd/daten/parkleitsystem.html"
city_name = "Zürich"
lat = 47.3666700
lon = 8.5500000

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

        lot = geodata.lot(title[0])
        data["lots"].append({
            "name": lot.name,
            "address": title[1],
            "id": lot.id,
            "state": summary[0],
            "free": summary[1],
            "total": lot.total,
            "coords": lot.coords,
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
