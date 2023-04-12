from bs4 import BeautifulSoup
from park_api.util import convert_date
from park_api.geodata import GeoData
from time import strptime, gmtime, mktime, strftime

geodata = GeoData(__file__)

def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")

    # suche Datum/Uhrzeit
    html_entry = soup.select("h3")
    date_time = strptime(html_entry[0].text.strip(), "Stand : %d.%m.%Y %H:%M:%S")
    last_updated = gmtime(mktime(date_time))
    data = {
        "last_updated": strftime("%Y-%m-%dT%H:%M:%S", last_updated),
        "lots": []
    }

    # suche die Zahlen zu den Parkhaeusern:
    html_table = soup.select("table")
    table_rows = html_table[0].find_all( "tr")
    for parking_lot in table_rows[1:]:
        lot_data = parking_lot.select("td")
        parking_name = lot_data[0].text.strip()
        # get the data from JSON-file:
        lot = geodata.lot(parking_name)

        try :
            if ( lot_data[3].text.strip() == "OK" ):
                parking_state = "open"
                parking_data = lot_data[1].text.split()
                parking_free = int(parking_data[0])
                parking_total = int(parking_data[2])
            else :
                parking_state = "nodata"
                parking_free = 0
                parking_total = lot.total
        except :
            parking_state = "nodata"
            parking_free = 0
            parking_total = lot.total

        data["lots"].append({
            "name":     parking_name,
            "free":     parking_free,
            "total":    parking_total,
            "address":  lot.address,
            "coords":   lot.coords,
            "state":    parking_state,
            "lot_type": lot.type,
            "id":       lot.id,
            "forecast": False,
        })

    return data
