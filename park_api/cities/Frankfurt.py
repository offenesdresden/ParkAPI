from bs4 import BeautifulSoup
from park_api.util import convert_date
from park_api.geodata import GeoData
import requests

# This loads the geodata for this city if <city>.geojson exists in the same directory as this file.
# No need to remove this if there's no geodata (yet), everything will still work.
geodata = GeoData(__file__)

# This function is called by the scraper and given the data of the page specified as source in geojson above.
# It's supposed to return a dictionary containing everything the current spec expects. Tests will fail if it doesn't ;)
def parse_html(html):

    # BeautifulSoup is a great and easy way to parse the html and find the bits and pieces we're looking for.
    soup = BeautifulSoup(html, "html.parser")
    r = requests.get('http://offenedaten.frankfurt.de/dataset/e821f156-69cf-4dd0-9ffe-13d9d6218597/resource/eac5ca3d-4285-48f4-bfe3-d3116a262e5f/download/parkdatensta.xml')
    geo = BeautifulSoup(r.text, "html.parser")
    # last_updated is the date when the data on the page was last updated, it should be listed on most pages
    last_updated = soup.find_all("publicationtime")[0].text.split(".")[0]


    data = {
        # convert_date is a utility function you can use to turn this date into the correct string format
        "last_updated": last_updated,
        # URL for the page where the scraper can gather the data
        "lots": []
    }
    for tr in soup.select("parkingfacilitytablestatuspublication > parkingfacilitystatus"):
        node = tr.find("parkingfacilityreference")
        lot_id = tr.find("parkingfacilityreference")["id"]
        lot_free = int(tr.find("totalnumberofoccupiedparkingspaces").text)
        lot_total = int(tr.find("totalparkingcapacityshorttermoverride").text)

        # please be careful about the state only being allowed to contain either open, closed or nodata
        # should the page list other states, please map these into the three listed possibilities
        state = tr.find("parkingfacilitystatus")
        if state and state.text in ["open", "closed"]:
            state = state.text
        else:
            state = "nodata"

        lotNode = geo.find(id=lot_id)
        if not lotNode:
            continue
        coordsNode = lotNode.find("pointcoordinates")

        lot = {
            "name": lotNode.find("parkingfacilitydescription").text,
            "address": "none",
            "coords": {"lng": float(coordsNode.find("longitude").text), "lat": float(coordsNode.find("latitude").text)},
            "type": "none",
            "id": lot_id
        }

        data["lots"].append({
            "name": lot["name"],
            "free": lot_free,
            "total": lot_total,
            "address": lot["address"],
            "coords": lot["coords"],
            "state": state,
            "lot_type": lot["type"],
            "id": lot["id"],
            "forecast": False,
        })
    return data
