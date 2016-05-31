import feedparser
from park_api.geodata import GeoData


# Falls das hier jemals einer von den Menschen
# hinter OpenDataZürich lesen sollte: Ihr seid so toll <3
geodata = GeoData(__file__)


def parse_html(xml_data):
    feed = feedparser.parse(xml_data)

    print(feed)