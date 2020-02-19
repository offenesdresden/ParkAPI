from bs4 import BeautifulSoup
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

    # last_updated is the date when the data on the page was last updated, it should be listed on most pages
    # Uhrzeit like Konstanz
    data = {
        # last_updated like Konstanz
        "last_updated": utc_now(),
        # URL for the page where the scraper can gather the data
        "lots": []
    }

    table = soup.find('table', id='haupttabelle')
    table2 = table.find('table', width='790')
    rows = table2.find_all('tr')
    for row in rows[3:12] :
        parking_data = row.find_all('td') 
        parking_name  = parking_data[0].text
        lot = geodata.lot(parking_name)
        try :
            parking_state = 'open'
            parking_free  = int(parking_data[2].text)
        except :
            parking_free  = 0
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
                "forecast": False,
            })

    return data
