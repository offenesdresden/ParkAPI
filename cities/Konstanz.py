from bs4 import BeautifulSoup
from util import convert_date
from geodata import GeoData

data_url = "http://www.konstanz.de/tourismus/01759/01765/"
city_name = "Konstanz"
file_name = "Konstanz"

total_number_map = {
    "Marktstätte": 268,
    "Altstadt": 359,
    "Lago": 930,
    "Augustiner / Karstadt": 284,
    "Fischmarkt": 158,
    "Döbele": 335,
    "Am Seerheim": 500,
    "Byk Gulden Str.": 100,
    "Benediktiner": 118,
    "Seerheincenter": 280
}

geodata = GeoData(city_name)


def parse_html(html):
    soup = BeautifulSoup(html)

    # last update time (UTC)
    update_time = soup.select('p > strong')[-1].text

    data = {
        "last_updated": convert_date(update_time, "Stand: %d.%m.%Y - %H:%M:%S"),
        "lots": []
    }

    # get all tables with lots
    raw_lot_list = soup.find_all("div", {"class": "listing"})

    # get all lots
    for lot_list in raw_lot_list:
        raw_lots = lot_list.select('tr + tr')

        for lot in raw_lots:
            lot_name = lot.select('a')[0].text

            try:
                lot_free = int(lot.select('td + td')[0].text)
            except ValueError:
                lot_free = 0

            data["lots"].append({
                "name": lot_name,
                "free": lot_free,
                "count": total_number_map.get(lot_name, 0),
                "coords": geodata.coords(lot_name)
            })

    return data
