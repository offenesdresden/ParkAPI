import os
import json

from park_api import env


def from_feature(feature):
    name = feature['properties']['name']
    lng, lat = feature['geometry']['coordinates']
    return name, {'lng': lng, 'lat': lat}


class GeoData:
    def __init__(self, city):
        json_file = city[:-3] + ".geojson"
        json_path = os.path.join(env.APP_ROOT, "park_api", "cities", json_file)
        try:
            with open(json_path) as f:
                geodata = json.load(f)
                self.lots = dict(map(from_feature, geodata['features']))
        except FileNotFoundError:
            geodata = self.lots = {}

    def coords(self, lot):
        return self.lots.get(lot, None)
