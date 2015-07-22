import os

import json
from collections import namedtuple
from park_api import env
from park_api.util import remove_special_chars


class Lot(namedtuple('Lot', ['name', 'id', 'type', 'lng', 'lat', 'address', 'total'])):
    @property
    def coords(self):
        if self.lng != None and self.lat != None:
            return {'lng': self.lng, 'lat': self.lat}
        return None


def generate_id(city, lot_name):
    """
    Generate an ID for a parking lot by concatenating city name and lot name.

    :param city: city name
    :param lot_name: Name of the parking lot
    :return: ID
    """
    _id = (city + lot_name).lower()
    return remove_special_chars(_id)


class GeoData:
    def __init__(self, city):
        json_file = city[:-3] + ".geojson"
        self.city = os.path.basename(city[:-3])
        json_path = os.path.join(env.APP_ROOT, "park_api", "cities", json_file)
        try:
            with open(json_path) as f:
                geodata = json.load(f)
                self.lots = dict(map(self.from_feature, geodata['features']))
        except FileNotFoundError:
            geodata = self.lots = {}
    def lot(self, name):
        lot = self.lots.get(name, None)
        if lot == None:
            _id = generate_id(self.city, name)
            return Lot(name, _id, None, None, None, None, 0)
        return lot
    def from_feature(self, feature):
        props = feature["properties"]
        name = props['name']
        if feature['geometry'] != None:
            lng, lat = feature['geometry']['coordinates']
        else:
            lng, lat = (None, None)
        address = props.get("address", None)
        total = props.get("total", 0)
        _type = props.get("type", None)
        _id = generate_id(self.city, name)
        return name, Lot(name, _id, _type, lng, lat, address, total)
