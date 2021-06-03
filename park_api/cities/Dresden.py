import os
import json
import time
import datetime
from bs4 import BeautifulSoup
from park_api.geodata import GeoData
from park_api.util import convert_date, get_most_lots_from_known_data

geodata = GeoData(__file__)


def parse_excell_api(html):
    api_data = json.loads(html)
    dt = time.strptime(api_data[0]["timestamp"].split(".")[0], "%Y-%m-%dT%H:%M:%S")
    ts = time.gmtime(time.mktime(dt))
    data = {
        "lots": [],
        "last_updated": time.strftime("%Y-%m-%dT%H:%M:%S", ts)
    }
    status = ['open', 'closed', 'unknown']
    id_lots = {geodata.lots[n].aux: geodata.lots[n] for n in geodata.lots}
    for dataset in api_data:
        try:
            lot = id_lots[dataset['id']]
            forecast = os.path.isfile("forecast_data/" + lot.id + ".csv")
            data["lots"].append({
                "coords": lot.coords,
                "name": lot.name,
                "total": lot.total,
                "free": max(lot.total - dataset["belegung"], 0),
                "state": status[dataset["status"] - 1],
                "id": lot.id,
                "lot_type": lot.type,
                "address": lot.address,
                "forecast": forecast,
                "region": ""
            })
        except KeyError:
            pass
    return data


# https://apps.dresden.de/ords/f?p=1110:1:0
def parse_website_app(html):
    soup = BeautifulSoup(html, "html.parser")
    date_field = soup.find(id="P1_LAST_UPDATE").text
    last_updated = convert_date(date_field, "%d.%m.%Y %H:%M:%S")
    data = {
        "lots": [],
        "last_updated": last_updated
    }

    for table in soup.find_all("table"):
        if table["summary"] != "":
            region = table["summary"]
            if region == "Busparkplätze":
                continue

            for lot_row in table.find_all("tr"):
                if lot_row.find("th") is not None:
                    continue

                cls = lot_row.find("div")["class"]
                state = "nodata"
                if "green" in cls or "yellow" in cls or "red" in cls:
                    state = "open"
                elif "park-closed" in cls:
                    state = "closed"

                lot_name = lot_row.find("td", {"headers": "BEZEICHNUNG"}).text

                try:
                    col = lot_row.find("td", {"headers": "FREI"})
                    free = int(col.text)
                except ValueError:
                    free = 0

                try:
                    col = lot_row.find("td", {"headers": "KAPAZITAET"})
                    total = int(col.text)
                except ValueError:
                    total = get_most_lots_from_known_data("Dresden", lot_name)

                lot = geodata.lot(lot_name)
                forecast = os.path.isfile("forecast_data/" + lot.id + ".csv")

                data["lots"].append({
                    "coords": lot.coords,
                    "name": lot_name,
                    "total": total,
                    "free": free,
                    "state": state,
                    "id": lot.id,
                    "lot_type": lot.type,
                    "address": lot.address,
                    "forecast": forecast,
                    "region": region
                })
    return data


# https://www.dresden.de/apps_ext/ParkplatzApp/index
def parse_website(html):
    soup = BeautifulSoup(html, "html.parser")
    for h3 in soup.find_all("h3"):
        if h3.text == "Letzte Aktualisierung":
            last_updated = convert_date(h3.find_next_sibling("div").text, "%d.%m.%Y %H:%M:%S")
    data = {
        "lots": [],
        "last_updated": last_updated
    }
    for table in soup.find_all("table"):
        thead = table.find("thead")
        if not thead:
            continue
        region = table.find("thead").find("tr").find_all("th")[1].find("div").text
        if region == "Busparkplätze":
            continue
        for tr in table.find("tbody").find_all("tr"):
            td = tr.find_all("td")
            name = tr.find("a").text
            lot = geodata.lot(name)
            try:
                total = int(td[2].find_all("div")[1].text)
            except ValueError:
                total = get_most_lots_from_known_data("Dresden", name)
            try:
                free = int(td[3].find_all("div")[1].text)
                valid_free = True
            except ValueError:
                valid_free = False
                free = 0
            if "park-closed" in td[0]["class"]:
                state = "closed"
            elif "blue" in td[0]["class"] and not valid_free:
                state = "nodata"
            else:
                state = "open"
            data["lots"].append({
                "coords": lot.coords,
                "name": name,
                "total": total,
                "free": free,
                "state": state,
                "id": lot.id,
                "lot_type": lot.type,
                "address": lot.address,
                "forecast": os.path.isfile("forecast_data/" + lot.id + ".csv"),
                "region": region
            })
    return data


def parse_html(html):
    if geodata.private_data:
        return parse_excell_api(html)
    else: #use website
        return parse_website(html)
