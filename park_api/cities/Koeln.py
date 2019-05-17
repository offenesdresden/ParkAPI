from bs4 import BeautifulSoup
from park_api.util import convert_date
from park_api.geodata import GeoData

# This loads the geodata for this city if <city>.geojson exists in the same directory as this file.
# No need to remove this if there's no geodata (yet), everything will still work.
geodata = GeoData(__file__)

# This function is called by the scraper and given the data of the page specified as source in geojson above.
# It's supposed to return a dictionary containing everything the current spec expects. Tests will fail if it doesn't ;)
def parse_html(html):
    # some helper-functions
    def calcLotsFree( td ):
        def calculate( value ):
            if value == 'X': return 0
            return int(value)
        
        images = td.find_all("img")
        if ( images[3]['alt'] == '-') : return -1
        free = calculate( images[0]['alt'])
        free = free*10 + calculate( images[1]['alt'])
        free = free*10 + calculate( images[2]['alt'])
        free = free*10 + calculate( images[3]['alt'])
        return free

#   go on with main-function
    # BeautifulSoup is a great and easy way to parse the html and find the bits and pieces we're looking for.
    soup = BeautifulSoup(html, "html.parser")

    # last_updated is the date when the data on the page was last updated, it should be listed on most pages
    # suche: <span class="datetime">07.05.2019 10:50</span></p>
    last_updated = soup.find( "span", class_="datetime").text

    data = {
        # convert_date is a utility function you can use to turn this date into the correct string format
        "last_updated": convert_date(last_updated, "%d.%m.%Y %H:%M"),
        # URL for the page where the scraper can gather the data
        "lots": []
    }

    # everything is in table-objects
    parking = soup.find_all( "table", class_="quarter")
    for car_park in parking :
        parking_quarter = car_park.find_all("tr")
        for parking_building in parking_quarter[1:] :
            car_parking  = parking_building.find_all("td")
            parking_name = car_parking[1].text
#            if   ('St. Martin (' in parking_name) : parking_name = 'Groß St. Martin (*)'
#            elif ( 'Hohe Stra' in parking_name)   : parking_name = 'Hohe Straße'
#            elif ( 'rzenich' in parking_name)     : parking_name = 'Gürzenich'
#            elif ( 'ln Arcaden' in parking_name)  : parking_name = 'Köln Arcaden'
#            elif ( 'ckenstra' in parking_name)    : parking_name = 'Brückenstraße'
#            elif ( 'cilienstra' in parking_name)  : parking_name = 'Cäcilienstraße'
#            elif ( 'Wolfsstra' in parking_name)   : parking_name = 'Wolfsstraße'
#            elif ( 'DuMont Carr' in parking_name) : parking_name = 'DuMont Carré'
#            elif ( 'ck/Mauspfad' in parking_name) : parking_name = 'Brück/Mauspfad'
            # get the data
            lot = geodata.lot(parking_name)
            # calc available parking_lots
            parking_state = 'open'
            parking_free = calcLotsFree( car_parking[0])
            if ( parking_free < 0 ) :
                parking_free = 0
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
