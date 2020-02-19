import os
from datetime import date
import calendar

import json
from collections import namedtuple
from park_api import env
from park_api.util import remove_special_chars


lot_fields = ['name', 'id', 'type', 'lng', 'lat', 'address', 'total', 'aux']


class Lot(namedtuple('Lot', lot_fields)):
    @property
    def coords(self):
        if self.lng is not None and self.lat is not None:
            return {'lng': self.lng, 'lat': self.lat}
        return None

city_fields = ['name', 'id', 'lng', 'lat', 'url', 'source', 'headers', 'public_source', 'active_support', 'attribution']


class City(namedtuple('City', city_fields)):
    @property
    def coords(self):
        if self.lng is not None and self.lat is not None:
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
            self.lots = {}
        private_file = city[:-3] + ".json"
        private_path = os.path.join(env.APP_ROOT, "park_api", "cities", private_file)
        try:
            with open(private_path) as p:
                self.private_data = json.load(p)
                self._process_private(self.private_data)
        except FileNotFoundError:
            self.private_data = None

    def _process_json(self, json):
        self.lots = {}
        self.city = None
        for f in json["features"]:
            self._process_feature(f)
        if self.city is None:
            self.city = City(self.city_name,
                             self.city_name,
                             None,
                             None,
                             None,
                             None,
                             None,
                             None)

    def _process_private(self, json):
        if self.city:
            self.city = City(self.city[0],
                             self.city[1], 
                             self.city[2],
                             self.city[3],
                             self.city[4],
                             json["source"],
                             json["public"],
                             self.city[7],
                             self.city[8])

    def _process_feature(self, feature):
        props = feature["properties"]
        _type = props.get("type", None)
        name = props["name"]
        lng, lat = self._coords(feature)
        if _type == "city":
            self.city = self._city_from_props(name, lng, lat, props)
        else:
            lot = self._lot_from_props(name, lng, lat, props)
            self.lots[name] = lot

    def _city_from_props(self, name, lng, lat, props):
        url = props.get("url", None)
        source = props.get("source", None)
        headers = props.get("headers", {})
        active_support = props.get("active_support", None)
        attribution = props.get("attribution", None)
        return City(name,
                    self.city_name,
                    lng,
                    lat,
                    url,
                    source,
                    headers,
                    source,
                    active_support,
                    attribution)

    def _lot_from_props(self, name, lng, lat, props):
        address = props.get("address", None)
        total = props.get("total", 0)
        if "total_by_weekday" in props.keys():
            weekday = calendar.day_name[date.today().weekday()]
            if weekday in props.get("total_by_weekday"):
                total = props.get("total_by_weekday").get(weekday)
        _type = props.get("type", None)
        _aux = props.get("aux", None)
        _id = generate_id(self.city_name + name)
        return Lot(name, _id, _type, lng, lat, address, total, _aux)

    def _coords(self, feature):
        geometry = feature.get("geometry", None)
        if geometry is None:
            return None, None
        else:
            lng, lat = geometry["coordinates"]
            return lng, lat

    def lot(self, name):
        lot = self.lots.get(name, None)
        if lot is None:
            _id = generate_id(self.city_name + name)
            return Lot(name, _id, None, None, None, None, 0, None)
        return lot
