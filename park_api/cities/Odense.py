from park_api.util import convert_date
from park_api.geodata import GeoData
import json
from datetime import datetime

# This loads the geodata for this city if <city>.geojson exists in the same directory as this file.
geodata = GeoData(__file__)


# This function is called by the scraper and given the data of the page specified as source in geojson above.
# It's supposed to return a dictionary containing everything the current spec expects. Tests will fail if it doesn't ;)
def parse_html(text_content):
    data_as_json = json.loads(text_content)

    # more data about the available parking spaces can be found at
    # http://odensedataplatform.dk/dataset/parkering

    # the service doesn't actually publish the last date it was updated,
    # so we will assume the data has just been updated
    last_updated = datetime.now().strftime("%d.%m.%Y %H:%M")
    data = {
        # convert_date is a utility function you can use to turn this date into the correct string format
        "last_updated": convert_date(last_updated, "%d.%m.%Y %H:%M"),
        "lots": []
    }

    for _, parking in data_as_json.items():
        lot_code = parking["idName"]
        name = parking["name"]
        total = parking["maxCount"]
        free = parking["freeCount"]

        # please be careful about the state only being allowed to contain either open, closed or nodata
        # should the page list other states, please map these into the three listed possibilities
        state = "nodata"

        lot = geodata.lot(lot_code)

        # this is to make sure that we don't include erroneous totals from the JSON file,
        # see the parking filosoffen_q_park_(ski_data) which outputs a total of 9999
        if lot.total < total:
            total = lot.total

        data["lots"].append({
            "name": name,
            "free": free,
            "total": total,
            "address": None,
            "coords": lot.coords,
            "state": state,
            "lot_type": lot.type,
            "id": lot.id,
            "forecast": False,
        })

    return data
