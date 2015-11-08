import os
import json
from park_api import env
from park_api.util import remove_special_chars
from .lot import Lot
from .city import City


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

    def _process_json(self, json):
        self.lots = {}
        self.city = None
        for f in json["features"]:
            self._process_feature(f)
        if self.city is None:
            self.city = City(self.city_name, self.city_name)

    def _process_feature(self, feature):
        props = feature["properties"]
        _type = props.get("type", None)
        name = props["name"]
        lng, lat = self._coords(feature)
        if _type == "city":
            self.city = City(name=name,
                             id=self.city_name,
                             lng=lng, lat=lat,
                             url=props.get("url", None),
                             source=props.get("source", None),
                             active_support=props.get("active_support", None))
        else:
            lot = Lot(name=name,
                      id=generate_id(self.city_name + name),
                      lng=lng,
                      lat=lat,
                      address=props.get("address", None),
                      total=props.get("total", 0),
                      lot_type=props.get("type", None),
                      free=None,
                      state=None)
            self.lots[name] = lot

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
            return Lot(name=name,
                       id=generate_id(self.city_name + name),
                       lot_type=None,
                       lng=None,
                       lat=None,
                       address=None,
                       state=None,
                       total=0,
                       free=0)
        return lot
