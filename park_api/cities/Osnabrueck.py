import copy
import datetime
import json
import re
from urllib import error, request

from park_api.util import convert_date
from park_api.geodata import GeoData

# This loads the geodata for this city if <city>.geojson exists in the same directory as this file.
# No need to remove this if there's no geodata (yet), everything will still work.
geodata = GeoData(__file__)

GEOMETRY_TEMPLATE = {"type": "Point",
                     "coordinates": [
                         0.0,
                         0.0
                     ]
                     }

PROPERTIES_TEMPLATE = {"name": "Parking Lot 1",
                       "total": 0,
                       "address": "Musterstraße 1",
                       "type": "Parkhaus"
                       }


def generate_geojson(html):
    parking_ramps, _ = get_general_info(html)

    osnabrueck = {"type": "Feature",
                  "geometry": {
                      "type": "Point",
                      "coordinates": [
                          8.05,
                          52.283333
                      ]
                  },
                  "properties": {
                      "name": "Osnabrueck",
                      "type": "city",
                      "url": "https://www.parken-osnabrueck.de/",
                      "source": "https://www.parken-osnabrueck.de/",
                      "active_support": False
                  }
                  },

    geojson = {}
    geojson['type'] = 'FeatureCollection'
    features = [osnabrueck,]

    for ramp in parking_ramps.values():
        properties = copy.deepcopy(PROPERTIES_TEMPLATE)
        geometry = copy.deepcopy(GEOMETRY_TEMPLATE)

        properties['name'] = ramp['name']
        properties['total'] = ramp['utilization']['total_capacity']
        properties['address'] = ramp['street']
        properties['type'] = 'unknown'

        geometry['coordinates'] = [ramp['longitude'],
                                   ramp['latitude']]

        feature = {'type': 'Feature',
                   'properties': properties,
                   'geometry': geometry}

        features.append(feature)

    geojson['features'] = features

    json.dump(geojson,
              'Osnabrueck.geojson')


def raise_for_status(response):
    """Raises stored :class:`HTTPError`, if one occurred.

    Taken from requests library.
    See: https://2.python-requests.org/en/master/_modules/requests/models/#Response.raise_for_status
    """

    http_error_msg = ""
    if isinstance(response.reason, bytes):
        # We attempt to decode utf-8 first because some servers
        # choose to localize their reason strings. If the string
        # isn't utf-8, we fall back to iso-8859-1 for all other
        # encodings. (See PR #3538)
        try:
            reason = response.reason.decode("utf-8")
        except UnicodeDecodeError:
            reason = response.reason.decode("iso-8859-1")
    else:
        reason = response.reason

    if 400 <= response.status < 500:
        http_error_msg = u"%s Client Error: %s for url: %s" % (
            response.status,
            reason,
            response.url,
        )

    elif 500 <= response.status < 600:
        http_error_msg = u"%s Server Error: %s for url: %s" % (
            response.status,
            reason,
            response.url,
        )

    if http_error_msg:
        raise error.HTTPError(
            url=response.geturl(),
            code=response.getcode(),
            msg=http_error_msg,
            hdrs=response.info(),
            fp=None,
        )


def get_details(url=None):
    with request.urlopen(url) as response:
        raise_for_status(response)
        page_source = response.read().decode()

    utilization = json.loads(page_source)

    utilization["access_time"] = convert_date(datetime.datetime.now(),
                                              "%d.%m.%Y %H:%M Uhr")

    return utilization


def get_general_info(html):
    page_source = html

    parking_ramps = re.search(
        pattern=r"var parkingRampData = (\{.*\});", string=page_source
    )

    parking_ramps = json.loads(html.unescape(parking_ramps.group(1)))

    utilization = get_details(
        r"https://www.parken-osnabrueck.de/index.php?type=427590&tx_tiopgparkhaeuserosnabrueck_parkingosnabruek[controller]=Parking&tx_tiopgparkhaeuserosnabrueck_parkingosnabruek[action]=ajaxCallGetUtilizationData&_=1556046149040"
    )

    for identifier, ramp_data in parking_ramps.items():
        details = utilization["ramp-" + identifier]

        ramp_data["utilization"] = {
            "free_capacity": details["available"],
            "total_capacity": details["capacity"],
        }

        del ramp_data["gmapsMarker"]

    return parking_ramps, utilization["access_time"]


# This function is called by the scraper and given the data of the page specified as source in geojson above.
# It's supposed to return a dictionary containing everything the current spec expects. Tests will fail if it doesn't ;)
def parse_html(html):
    parking_ramps, access_time = get_general_info(html)

    data = {
        # convert_date is a utility function you can use to turn this date into the correct string format
        "last_updated": access_time,
        # URL for the page where the scraper can gather the data
        "lots": []
    }

    for ramp in parking_ramps:
        lot_name = ramp['name']
        lot_free = ramp['utilization']['free_capacity']
        lot_total = ramp['utilization']['total_capacity']

        # please be careful about the state only being allowed to contain either open, closed or nodata
        # should the page list other states, please map these into the three listed possibilities
        state = 'nodata'

        lot = geodata.lot(lot_name)
        data["lots"].append({
            "name": lot.name,
            "free": lot_free,
            "total": lot_total,
            "address": lot.address,
            "coords": lot.coords,
            "state": state,
            "lot_type": lot.type,
            "id": lot.id,
            "forecast": False,
        })

    return data
