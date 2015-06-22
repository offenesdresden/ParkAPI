from bs4 import BeautifulSoup
import datetime
import pytz

data_url = "http://kwlpls.adiwidjaja.info"
city_name = "Lübeck"
file_name = "Luebeck"


def parse_html(html):
    soup = BeautifulSoup(html)
    data = {
        "lots": []
    }

    # get time last updated
    last_updated = datetime.datetime.strptime(soup.find("tr").find("strong").text, "Stand: %d.%m.%Y, %H:%M Uhr")

    local_timezone = pytz.timezone("Europe/Berlin")

    last_updated = local_timezone.localize(last_updated, is_dst=None)
    last_updated = last_updated.astimezone(pytz.utc).replace(tzinfo=None)

    data["last_updated"] = last_updated.replace(microsecond=0).isoformat()

    rows = soup.find_all("tr")
    rows = rows[1:]
    i = -1  # index for current region
    for row in rows:
        if len(row.find_all("th")) > 0:
            # This is a header row, save it for later
            region_header = row.find("th", {"class": "head1"}).text
            # data["lots"][region_header] = []
            data["lots"].append({
                "name": region_header,
                "lots": []
            })
            i += 1
        else:
            if row.find("td").text == "Gesamt":
                continue
            # This is a parking lot row
            raw_lot_data = row.find_all("td")
            if len(raw_lot_data) == 2:
                data["lots"][i]["lots"].append({
                    "name": raw_lot_data[0].text
                })
            elif len(raw_lot_data) == 4:
                data["lots"][i]["lots"].append({
                    "name": raw_lot_data[0].text,
                    "count": int(raw_lot_data[1].text),
                    "free": int(raw_lot_data[2].text)
                })
    return data


if __name__ == "__main__":
    file = open("../tests/luebeck.html")
    html_data = file.read()
    file.close()
    parse_html(html_data)
