
import requests
from bs4 import BeautifulSoup as soup
import re
from park_api.util import convert_date
from park_api.geodata import GeoData

# This loads the geodata for this city if <city>.geojson exists in the same directory as this file.
# No need to remove this if there's no geodata (yet), everything will still work.
geodata = GeoData(__file__)

# source url https://pls.marburg.de/
my_url = ('https://pls.marburg.de/')

# Gesamtanzahl der Parkplätze: https://www.marburg.de/smartcity/10/03/01/index.html
# unter dem link gibt es weitere Parkplätze ohne aktuelle Informationen und die Gesamtkapazität

# store page in var
r = requests.get(my_url)

# parse the html-page in the var using an html parser of the beautiful soup package
page_soup = soup(r.text, "html.parser")


# This function is called by the scraper and given the data of the page specified as source in geojson above.
# It's supposed to return a dictionary containing everything the current spec expects. Tests will fail if it doesn't ;)
def parse_html(html):

    # BeautifulSoup is a great and easy way to parse the html and find the bits and pieces we're looking for.
    soup = BeautifulSoup(html, "html.parser")

    # last_updated is the date when the data on the page was last updated, it should be listed on most pages
    last_updated = convert_date(fetch_day[0] + " " + fetch_time[0], '%d.%m.%Y %H:%M:%S')

    # Regulärer Ausdruck für das Datum: [0-3][0-9].[0-9][0-9].20[0-9][0-9]
    fetch_day = re.findall("[0-3][0-9].[0-9][0-9].20[0-9][0-9]", str(page_soup.body.text))

    # Reulärer Ausdruck für die Uhrzeit: [0-2][0-9]:[0-5][0-9]:[0-9][0-9]
    fetch_time = re.findall("[0-2][0-9]:[0-5][0-9]:[0-9][0-9]", str(page_soup.body.text))

    data = {
        # convert_date is a utility function you can use to turn this date into the correct string format
        "last_updated": convert_date(last_updated, "%d.%m.%Y %H:%M Uhr"),
        # URL for the page where the scraper can gather the data
        "lots": []
    }

    for row in page_soup.table.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) == 4:
            lot_name = re.sub("\s+-\s+geschlossen", "", cells[0].text)
            lot_name = re.sub("[\n\t]+", "", lot_name)

            lot_name = re.sub(" +", " ", lot_name)
            lot_free = int(re.sub("[^0-9]", "", cells[1].text) or 0)

            if "geschlossen" in cells[0].text:
                state = 'closed'
            else:
                state = 'open'

        lot = geodata.lot(lot_name)
        data["lots"].append({
            "name": lot.name,
            "free": lot_free,
            "total": lot_total,
            "address": lot.address,
            "coords": lot.coords,
            "state": state,
            "lot_type": lot.type,
            "id": lot.id,
            "forecast": False,
        })

    return data

