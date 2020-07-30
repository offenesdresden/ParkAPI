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

    # suche: <div id="parkhausliste-ct">
    div_level1 = soup.find_all('div', id='parkhausliste-ct')[-1]
    # <p style="color: #7a7a7b; padding: 18px 0 8px 0">zuletzt aktualisiert am 19.06.2019, 15:27 Uhr</p>
    date_time = div_level1.find('p')
    data['last_updated'] = convert_date(date_time.text, 'zuletzt aktualisiert am %d.%m.%Y, %H:%M Uhr')

    # find all entries:
    div_level2 = div_level1.find('div')
    div_level3 = div_level2.find_all('div')
    count = 0
    while (count < len(div_level3)-2) : 
        parking_name = div_level3[count+1].text.strip()
        lot = geodata.lot(parking_name)
        parking_free = 0
        parking_state = 'open'
        try :
            parking_free = int(div_level3[count+2].text)
        except :
            parking_state = 'nodata'
        count += 3

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

