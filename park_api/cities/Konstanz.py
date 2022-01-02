from bs4 import BeautifulSoup
from park_api.util import convert_date, utc_now
from park_api.geodata import GeoData
import datetime

geodata = GeoData(__file__)


def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")

    # last update time (UTC)
    # Konstanz does not support the last_updated yet. I hope they will inform me when it's added
    # as the data seems accurate I will return the current time and date
    data = {
        "last_updated": utc_now(),
        "lots": []
    }

    # get all tables with lots
    parken = soup.find_all( "table", class_="parken")

    # get all lots
    for park_lot in parken :
        td = park_lot.find_all("td")
        parking_name = td[0].text.strip()
        if parking_name == "Parkmöglichkeit":
            continue
        # work-around for the Umlaute-problem: ugly but working
        if ( 'Marktst' in parking_name) : parking_name = 'Marktstätte'
        elif ( 'bele' in parking_name) : parking_name = 'Döbele'
        # get the data
        lot = geodata.lot(parking_name)
        # look for free lots
        parking_state = 'open'
        parking_free  = 0
        try:
            parking_free = int(td[1].text)
        except:
            parking_state = 'nodata'

        data["lots"].append({
            "name":     parking_name,
            "free":     parking_free,
            "total":    lot.total,
            "address":  lot.address,
            "coords":   lot.coords,
            "state":    parking_state,
            "lot_type": lot.type,
            "id":       lot.id,
            "forecast": False
        })

    return data
