import os
import json
cities_path = os.path.dirname(os.path.realpath(__file__))

class GeoData:
    def __init__(self, city):
        lots = {}
        json_path = os.path.join(cities_path, "cities", city + ".geojson")
        with open(json_path) as f:
          geodata = json.load(f)
          for feature in geodata["features"]:
              lots[feature["properties"]["name"]] = {
                      "lon": feature["geometry"]["coordinates"][0],
                      "lat": feature["geometry"]["coordinates"][1]
                      }
          self.lots = lots
    def coords(self, lot):
        return self.lots.get(lot, [])
