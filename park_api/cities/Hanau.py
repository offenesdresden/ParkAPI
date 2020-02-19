from bs4 import BeautifulSoup
from park_api.util import convert_date
from park_api.geodata import GeoData
from park_api.util import utc_now

# This loads the geodata for this city if <city>.geojson exists in the same directory as this file.
# No need to remove this if there's no geodata (yet), everything will still work.
geodata = GeoData(__file__)

# This function is called by the scraper and given the data of the page specified as source in geojson above.
# It's supposed to return a dictionary containing everything the current spec expects. Tests will fail if it doesn't ;)
def parse_html(html):

    # BeautifulSoup is a great and easy way to parse the html and find the bits and pieces we're looking for.
    soup = BeautifulSoup(html, "html.parser")

    data = {
        "last_updated": '',
        # URL for the page where the scraper can gather the data
        "lots": []
    }

    try :
        # <div class="container-fluid"
        parking_data = soup.find( 'div', class_='container-fluid')
        # Letzte Aktualisierung: 04.07.2019 11:03:00
        last_updated = convert_date( parking_data.find('h5').text, 'Letzte Aktualisierung: %d.%m.%Y %H:%M:%S')
        data["last_updated"] = last_updated
    except :
        # if the service is unavailable (did happen in one of my tests):
        data["last_updated"] = utc_now()
        # return data

    parking_lots = parking_data.find_all('div', class_='well')
    for one_parking_lot in parking_lots :
        parking_name = one_parking_lot.find('b').text.strip()
        lot = geodata.lot(parking_name)
        parking_free = 0
        try :
            parking_status = 'open'
            parking_free = int(one_parking_lot.find_all('div', role='progressbar')[1].find('b').text.strip())
        except :
            parking_status = 'nodata'

        data["lots"].append({
                    "name":     parking_name,
                    "free":     parking_free,
                    "total":    lot.total,
                    "address":  lot.address,
                    "coords":   lot.coords,
                    "state":    parking_status,
                    "lot_type": lot.type,
                    "id":       lot.id,
                    "forecast": False
                })

    return data

