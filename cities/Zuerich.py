import feedparser
import requests

data_url = "http://www.pls-zh.ch/plsFeed/rss"

city_name = "Zürich"
file_name = "Zuerich"


def parse_html(data):
    feed = feedparser.parse(data)

    data = {
        "lots": [],
        "last_updated": feed["entries"][0]["updated"]
    }

    for entry in feed["entries"]:
        summary = parse_summary(entry["summary"])
        state = summary[0]
        free = summary[1]

        data["lots"].append({
            "name": entry["title"],
            "id": entry["id"].split("=")[1],
            "free": free,
            "state": state
        })

    return data


def parse_summary(summary):
    """Parse a string from the format 'open /   41' into both its params"""
    summary = summary.split("/")
    summary[0] = summary[0].strip()
    summary[1] = int(summary[1])
    return summary


if __name__ == "__main__":
    r = requests.get(data_url)
    parse_html(r.text)
