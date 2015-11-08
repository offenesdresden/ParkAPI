import feedparser
from park_api.util import parse_date
from park_api.models import GeoData, Lots

# Falls das hier jemals einer von den Menschen
# hinter OpenDataZürich lesen sollte: Ihr seid so toll <3
geodata = GeoData(__file__)


def parse_html(xml_data):
    feed = feedparser.parse(xml_data)

    lots = Lots()
    updated_at = parse_date(feed["entries"][0]["updated"],
                            "%Y-%m-%dT%H:%M:%SZ")

    for entry in feed["entries"]:
        state, free = parse_summary(entry["summary"])
        name, address, type_ = parse_title(entry["title"])

        identifier = ("%s %s" % (name, type_)).strip()
        lot = geodata.lot(identifier)
        lot.name = name
        lot.address = address
        lot.state = state
        lot.free = free
        lot.lot_type = type_
        lot.updated_at = updated_at
        lots.append(lot)

    return lots


def parse_summary(summary):
    """Parse a string from the format 'open /   41' into both its params"""
    summary = summary.split("/")

    state = summary[0].strip()
    if "?" in summary[0]:
        state = "nodata"

    s = summary[1].strip()
    if "?" in s:
        free = 0
    else:
        free = int(s)
    return state, free


def parse_title(title):
    """
    Parse a string from the format 'Parkgarage am Central / Seilergraben'
    into both its params
    """
    types = ["Parkhaus", "Parkplatz"]

    name = title.split(" / ")[0]
    address = title.split(" / ")[1]
    type = ""
    if name.split(" ")[0] in types:
        type = name.split(" ")[0]
        name = " ".join(name.split(" ")[1:])

    return name, address, type
