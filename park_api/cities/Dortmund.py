from bs4 import BeautifulSoup
from park_api.util import convert_date
from park_api.geodata import GeoData

# This loads the geodata for this city if <city>.geojson exists in the same directory as this file.
# No need to remove this if there's no geodata (yet), everything will still work.
geodata = GeoData(__file__)

# This function is called by the scraper and given the data of the page specified as source in geojson above.
# It's supposed to return a dictionary containing everything the current spec expects. Tests will fail if it doesn't ;)
def parse_html(html):

    # BeautifulSoup is a great and easy way to parse the html and find the bits and pieces we're looking for.
    soup = BeautifulSoup(html, "html.parser")

    # last_updated is the date when the data on the page was last updated, it should be listed on most pages
    last_updated = soup.find('h2').text

    data = {
        # convert_date is a utility function you can use to turn this date into the correct string format
        #                                          Stand: 07.06.2019 15:46 Uhr
        "last_updated": convert_date(last_updated, "Stand: %d.%m.%Y %H:%M Uhr"),
        # URL for the page where the scraper can gather the data
        "lots": []
    }

    # find all entries
    all_parking_lots = soup.find_all('dl')
    for parking_lot in all_parking_lots : 
        parking_name = parking_lot.find('dt').text
        lot = geodata.lot(parking_name)

        try :
            parking_state = 'open'
            parking_free = int(parking_lot.find('dd').find('strong').text)
        except :
            parking_state = 'nodata'
            parking_free = 0

        data["lots"].append({
                "name":     parking_name,
                "free":     parking_free,
                "total":    lot.total,
                "address":  lot.address,
                "coords":   lot.coords,
                "state":    parking_state,
                "lot_type": lot.type,
                "id":       lot.id,
                "forecast": False,
            })

    return data
