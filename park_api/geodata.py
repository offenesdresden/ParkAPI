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


class City(namedtuple('City', ['name', 'id', 'lng', 'lat', 'url', 'source'])):
    @property
    def coords(self):
        if self.lng != None and self.lat != None:
            return {'lng': self.lng, 'lat': self.lat}
        return None


def generate_id(s):
    return remove_special_chars(s.lower())


class GeoData:
    def __init__(self, city):
        json_file = city[:-3] + ".geojson"
        self.city_name = os.path.basename(city[:-3])
        json_path = os.path.join(env.APP_ROOT, "park_api", "cities", json_file)
        try:
            with open(json_path) as f:
                self._process_json(json.load(f))
        except FileNotFoundError:
            geodata = self.lots = {}

    def _process_json(self, json):
        self.lots = {}
        self.city = None
        for f in json["features"]:
            self._process_feature(f)
        if self.city == None:
            self.city = City(self.city_name, self.city_name, None, None, None, None)
    def _process_feature(self, feature):
        props = feature["properties"]
        _type = props.get("type", None)
        name  = props["name"]
        lng, lat = self._coords(feature)
        if _type == "city":
            self.city = self._city_from_props(name, lng, lat, props)
        else:
            lot = self._lot_from_props(name, lng, lat, props)
            self.lots[name] = lot

    def _city_from_props(self, name, lng, lat, props):
        url = props.get("url", None)
        source = props.get("source", None)
        return City(name, self.city_name, lng, lat, url, source)

    def _lot_from_props(self, name, lng, lat, props):
        address = props.get("address", None)
        total = props.get("total", 0)
        _type = props.get("type", None)
        _id = generate_id(self.city_name + name)
        return Lot(name, _id, _type, lng, lat, address, total)

    def _coords(self, feature):
        geometry = feature.get("geometry", None)
        if geometry == None:
            return None, None
        else:
            lng, lat = geometry["coordinates"]
            return lng, lat

    def lot(self, name):
        lot = self.lots.get(name, None)
        if lot == None:
            _id = generate_id(self.city_name + name)
            return Lot(name, _id, None, None, None, None, 0)
        return lot
