import os
import json


def from_feature(feature):
    name = feature['properties']['name']
    lng, lat = feature['geometry']['coordinates']
    return name, {'lng': lng, 'lat': lat}


class GeoData:
    def __init__(self, city):
        json_path = os.path.join(city[:-3] + ".geojson")
        try:
            with open(json_path) as f:
                geodata = json.load(f)
                self.lots = dict(map(from_feature, geodata['features']))
        except FileNotFoundError:
            geodata = self.lots = {}

    def coords(self, lot):
        return self.lots.get(lot, None)
