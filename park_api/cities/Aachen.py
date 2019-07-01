from bs4 import BeautifulSoup
# from park_api.util import convert_date
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
        "last_updated": utc_now(),     # not found on site, so we use something else
        # URL for the page where the scraper can gather the data
        "lots": []
    }
    # for handling duplicate entries
    dataUniqe = dict()

    # find all entries:
    # suche <div class="houses">
    parking_houses = soup.find_all('div', class_='houses')
    for parking_group in parking_houses :
        parking_lots = parking_group.find_all('li') 
        for one_lot in parking_lots :
            parking_name = one_lot.find('a').text
            if ( not parking_name in dataUniqe ) :
                dataUniqe[parking_name] = 1    # add this to the list
                lot = geodata.lot(parking_name)

                parking_state = 'open'
                parking_free = 0
                try :
                    parking_free = int(one_lot.find('span', class_='free-text').text.split()[0])
                except :
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

