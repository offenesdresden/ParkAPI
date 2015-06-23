import feedparser

data_url = "http://www.pls-zh.ch/plsFeed/rss"

city_name = "Zürich"
file_name = "Zuerich"

# Falls das hier jemals einer von den Menschen hinter OpenDataZürich lesen sollte: Ihr seid so toll <3

def parse_html(xml_data):
    feed = feedparser.parse(xml_data)

    data = {
        "lots": [],
        "last_updated": feed["entries"][0]["updated"]
    }

    for entry in feed["entries"]:
        summary = parse_summary(entry["summary"])
        title = parse_title(entry["title"])

        data["lots"].append({
            "name": title[0],
            "address": title[1],
            "id": entry["id"].split("=")[1],
            "state": summary[0],
            "free": summary[1]
        })

    return data


def parse_summary(summary):
    """Parse a string from the format 'open /   41' into both its params"""
    summary = summary.split("/")

    summary[0] = summary[0].strip()
    if "?" in summary[0]:
        summary[0] = "unknown"

    try:
        summary[1] = int(summary[1])
    except ValueError:
        summary[1] = 0
    return summary


def parse_title(title):
    """Parse a string from the format 'Parkgarage am Central / Seilergraben' into both its params"""
    title = title.split(" / ")
    return title
