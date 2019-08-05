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

    data = {
        "last_updated": '',     # will fill this later
        # URL for the page where the scraper can gather the data
        "lots": []
    }

    #                                                                        Datum: 22.07.2019 - Uhrzeit: 16:57
    data['last_updated'] = convert_date( soup.find('div', class_='col-sm-12').text, 'Datum: %d.%m.%Y - Uhrzeit: %H:%M')

    parking_lots = soup.find_all( 'div', class_='row carparkContent')
    for one_parking_lot in parking_lots :
        park_temp1 = one_parking_lot.find( 'div', class_='carparkLocation col-sm-9')
        park_temp2 = park_temp1.find('a')
        if ( park_temp2 != None ) :
            parking_name = park_temp2.text
        else :
            parking_name = park_temp1.text.strip()
        lot = geodata.lot(parking_name)

        parking_free = 0
        parking_state = 'open'
        try :
            # text: Freie Parkplätze: 195
            parking_free_temp = one_parking_lot.find('div', class_='col-sm-5').text.split()
            # parking_free_temp: ['Freie', 'Parkplätze:', '195']
            parking_free = int(parking_free_temp[2])
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

