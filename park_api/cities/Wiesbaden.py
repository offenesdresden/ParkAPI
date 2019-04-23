from bs4 import BeautifulSoup
from park_api.util import convert_date
from park_api.geodata import GeoData

geodata = GeoData(__file__)

def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")

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
        "last_updated": convert_date(last_updated, "%d.%m.%Y %H:%M"),
        "lots": []
    }

    table=soup.select('table')
    td = table[2].find_all('td')
    i = 0
    while i < len(td)-4 :
        parking_name = td[i+1].text.strip()
        lot = geodata.lot(parking_name)
        try:
            parking_state = 'open'
            parking_free  = 0
            parking_total = 0
            if ( 'geschlossen' in td[i+2].text ) :
                parking_state = 'closed'
            else :
                parking_free = int(td[i+2].text.split()[0])
                parking_total = int(td[i+2].text.split()[2])
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
        i += 5    # next parking-lot

    return data
