__author__ = 'kilian'

from bs4 import BeautifulSoup
import datetime

data_url = "http://www.ingolstadt.mobi/parkplatzauskunft.cfm"
city_name = "Ingolstadt"
file_name = "Ingolstadt"

def parse_html(html):
    soup = BeautifulSoup(html)

    # get time last updated
    data = {
        "last_updated": str(datetime.datetime.strptime(soup.p.string, "(%d.%m.%Y, %H.%M Uhr)")),
        "lots": []
    }

    # get all lots
    raw_lots = soup.find_all("tr")

    for lot in raw_lots:
        elements = lot.find_all("td")

        data["lots"].append({
            "name": elements[0].text,
            "free": int(elements[1].text)
        })

    return data
