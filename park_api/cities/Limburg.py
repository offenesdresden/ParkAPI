from bs4 import BeautifulSoup
from park_api.util import convert_date
from park_api.geodata import GeoData
# from park_api.util import utc_now

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

    #                                                       <b>Stand: 13.08.2019 16:40:00 Uhr</b> (Aktualisierung alle 60 Sekunden)<br>
    data['last_updated'] = convert_date( soup.find('b').text, 'Stand: %d.%m.%Y %H:%M:%S Uhr') 

    entries = soup.find( 'table', class_= 'tabellenformat')
    entries_rows = entries.find_all( 'tr' )
    # first line: header
    for one_entry in entries_rows[1:] :
        one_entry_data = one_entry.find_all( 'td')
        parking_name = one_entry_data[0].text
        lot = geodata.lot(parking_name)

        parking_free = 0
        parking_total = 0
        try :
            parking_total = int(one_entry_data[1].text)
            if ( one_entry_data[5].text.__eq__('Offen') ) : 
                parking_status = 'open'
                parking_free = int(one_entry_data[3].text)
            elif ( one_entry_data[5].text.__eq__('Geschlossen') ) : 
                parking_status = 'closed'
            else :
                parking_status = 'nodata'
        except :
            parking_status = 'nodata'
            
        data["lots"].append({
                    "name":     parking_name,
                    "free":     parking_free,
                    "total":    parking_total,
                    "address":  lot.address,
                    "coords":   lot.coords,
                    "state":    parking_status,
                    "lot_type": lot.type,
                    "id":       lot.id,
                    "forecast": False
                })

    return data

