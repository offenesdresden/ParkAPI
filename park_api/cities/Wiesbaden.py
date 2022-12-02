from bs4 import BeautifulSoup
from park_api.util import convert_date
from park_api.geodata import GeoData

geodata = GeoData(__file__)

def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")

    # suche Datum/Uhrzeit
    html_entry = soup.select("h3")
    date_time = html_entry[0].text
    last_updated = date_time[10:26]
    data = {
        "last_updated": last_updated,
        "lots": []
    }

    # suche die Zahlen zu den Parkhaeusern:
    html_table = soup.select("table")
    table_rows = html_table[0].select( "tr")
    for parking_lot in table_rows[1:] :
        lot_data = parking_lot.select("td")
        parking_name = lot_data[0].text
        # get the data from JSON-file:
        lot = geodata.lot(parking_name)

        try :
            if ( lot_data[3].text.strip() == "OK" ):
                parking_state = "open"
                parking_data = lot_data[1].text.split()
                parking_free = parking_data[0]
                parking_total = parking_data[2]
            else :
                parking_state = "nodata"
                parking_free = 0
                parking_total = 0
        except :
            parking_state = "nodata"
            parking_free = 0
            parking_total = 0

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
