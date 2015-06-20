from bs4 import BeautifulSoup
import datetime

data_url = "http://kwlpls.adiwidjaja.info"
city_name = "Lübeck"
file_name = "Luebeck"


def parse_html(html):
    soup = BeautifulSoup(html)
    data = {
        "lots": {}
    }

    # get time last updated
    date_last_changed = datetime.datetime.strptime(soup.find("tr").find("strong").text, "Stand: %d.%m.%Y, %H:%M Uhr")
    data["last_changed"] = str(date_last_changed)

    rows = soup.find_all("tr")
    rows = rows[1:]  #
    for row in rows:
        if len(row.find_all("th")) > 0:
            # This is a header row, save it for later
            region_header = row.find("th", {"class": "head1"}).text
            data["lots"][region_header] = []
        else:
            if row.find("td").text == "Gesamt":
                continue
            # This is a parking lot row
            raw_lot_data = row.find_all("td")
            if len(raw_lot_data) == 2:
                data["lots"][region_header].append({
                    "name": raw_lot_data[0].text
                })
            elif len(raw_lot_data) == 4:
                data["lots"][region_header].append({
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
