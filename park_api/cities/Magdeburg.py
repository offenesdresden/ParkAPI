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
        "last_updated": '',  # will add this later
        # URL for the page where the scraper can gather the data
        "lots": []
    }

    # find all entries
    outer_table = soup.find('table')
    # first group of lots
    inner_tables = outer_table.find_all('table')
    # inner_tables[0] ist Navi-Leiste, weiter mit first_part[1] 
    rows = inner_tables[1].find_all('tr')
    for row in rows[6:] :
        one_row = row.find_all('td')
        if ( one_row[0].text == '' ) : continue
        #
        if ( len(one_row) <= 5 ) :
            startingPoint = 0
        else :
            startingPoint = 1
        parking_name = one_row[startingPoint+0].text.strip()
        lot = geodata.lot(parking_name)
        try :
            parking_free = 0
            if ( 'offline' == one_row[startingPoint+1].text.strip() ) :
                parking_status = 'nodata'
            else :
                parking_status = 'open'
                parking_free = int(one_row[startingPoint+1].text)
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
                "forecast": False,
            })
   
    # second group of lots
    rows = inner_tables[2].find_all('tr')
    for row in rows[4:9] :
        one_row = row.find_all('td')
        if ( one_row[0].text == '' ) : continue
        #
        if ( len(one_row) <= 2  ) :
            startingPoint = 0
        else :
            startingPoint = 1
        parking_name = one_row[startingPoint+0].text.strip()
        lot = geodata.lot(parking_name)
        if ( lot.address == None ) : print('not found: ', '/'+parking_name+'/')
        try :
            parking_free = 0
            if ( 'offline' == one_row[startingPoint+1].text.strip() ) :
                parking_status = 'nodata'
            else :
                parking_status = 'open'
                parking_free = int(one_row[startingPoint+1].text)
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
                "forecast": False,
            })

    # finaly we set the last_updated field
    #   <font color="grey" face="Arial" size="1">Letzte Aktualisierung vom 12.06.2019 11:22 Uhr</font>
    current_date = rows[10].text.split()
    data["last_updated"] = convert_date(current_date[12]+' '+current_date[13], '%d.%m.%Y %H:%M')

    return data
