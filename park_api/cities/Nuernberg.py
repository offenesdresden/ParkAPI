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
    # suche:  <td width="233">
    date_time_text = soup.find('td', width='233').text.strip()

    data = {
        # convert_date is a utility function you can use to turn this date into the correct string format
        #                                            'Stand vom 05.06.2019, 14:40:20'
        "last_updated": convert_date(date_time_text, 'Stand vom %d.%m.%Y, %H:%M:%S'),
        # URL for the page where the scraper can gather the data
        "lots": []
    }

    # everything is in table-objects
    # so we have to go down several levels of table-objects
    html_level0 = soup.find('table')
    html_level1 = html_level0.find_all( 'table')
    html_level2 = html_level1[1].find_all('table')
    html_level3 = html_level2[0].find_all('table')
    html_level4 = html_level3[2].find_all('table')
    # here we have the data of the tables
    #   [0]: header
    #   [1]: empty
    #   all following: empty or Parkhaus
    for html_parkhaus in html_level4[2:] :
        if ( html_parkhaus.text.strip() == '' ) : continue   # table is empty
        html_parkhaus_all_rows = html_parkhaus.find_all('tr')
        for html_parkhaus_row in html_parkhaus_all_rows :
            # one row: one parkhaus
            html_parkhaus_data = html_parkhaus_row.find_all('td')
            parking_name_list = html_parkhaus_data[1].text.split()
            parking_name = ''
            for parking_name_part in parking_name_list :
                if ( parking_name != '' ) : parking_name += ' '
                parking_name += parking_name_part

            lot = geodata.lot(parking_name)
            parking_state = 'open'
            parking_free  = 0
            try :
                parking_free = int(html_parkhaus_data[2].text)
            except:
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
