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
    stand=soup.select('span')    
    # this gives you:
    # in stand[0]: <span style="font-weight: normal; letter-spacing: 0px;">
    #              Stand: 10.04.2019 15:09        </span>
    # splitting it gives you: u'10.04.2019', u'15:09'
    # putting it together: u'10.04.2019  15:09'
    last_updated_date=stand[0].text.strip().split()[1]
    last_updated_time=stand[0].text.strip().split()[2]
    last_updated = last_updated_date + "  " + last_updated_time

    data = {
        # convert_date is a utility function you can use to turn this date into the correct string format
        "last_updated": convert_date(last_updated, "%d.%m.%Y %H:%M"),
        # URL for the page where the scraper can gather the data
        "lots": []
    }

    table=soup.select('table')
    td = table[2].find_all('td')
    i = 0
    while i < len(td)-4 :
        j = i     # simplifies error-handling
        i += 5    # next parking-lot
        parking_name = td[j+1].text.strip()
        lot = geodata.lot(parking_name)
        try:
            parking_state = 'open'
            parking_free  = 0
            parking_total = 0
            if ( 'geschlossen' in td[j+2].text ) : 
                parking_state = 'closed'
            else :
                parking_free = int(td[j+2].text.split()[0])
                parking_total = int(td[j+2].text.split()[2])
        except:
            parking_state = 'nodata'

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
