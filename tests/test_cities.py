import os
import unittest
import ddt
import helpers
import importlib
from datetime import datetime
from park_api import db, env, security


def scrape_city(city):
    allowed_extensions = [".html", ".json", ".xml"]
    for extension in allowed_extensions:
        path = os.path.join(helpers.TEST_ROOT,
                            "fixtures",
                            city.lower() + extension)
        if os.path.isfile(path):
            break
    with open(path, 'rb') as f:
        city = importlib.import_module("park_api.cities." + city)
        return city.parse_html(f.read().decode('utf-8', 'replace'))

def get_tests():
    modpath = os.path.join(env.APP_ROOT, "park_api", "cities")
    strip_py = lambda name: ".".join(name.split(".")[:-1])
    for (dirpath, dirnames, filenames) in os.walk(modpath):
        return tuple(map(strip_py, filter(security.file_is_allowed, filenames)))

@ddt.ddt
class CityTestCase(unittest.TestCase):
    def setUp(self):
        db.setup()

    def sanity_check(self, city_name, city):
        self.assertIn("lots", city)
        self.assertIn("last_updated", city)
        last_updated = datetime.strptime(city["last_updated"],
                                         "%Y-%m-%dT%H:%M:%S")
        self.assertIsInstance(last_updated, datetime)

        self.assertTrue(len(city["lots"]) > 0)

        for lot in city["lots"]:
            self.assertIn("name", lot)

            self.assertIn("coords", lot)

            self.assertIn("state", lot)
            self.assertIn(lot["state"],
                          ["open", "closed", "nodata", "unknown"])

            self.assertIn("id", lot)

            self.assertIn("forecast", lot)
            self.assertIs(type(lot["forecast"]), bool)

            self.assertIn("free", lot)
            self.assertIn("total", lot)
            total, free = lot["total"], lot["free"]
            if total < free:
                msg = "\n[warn] total lots should be more than free lots:"\
                      " %d >= %d: %s => %s"
                print(msg % (total, free, city_name, lot))
            if "coords" in lot and lot["coords"] is not None:
                self.assertIn("lat", lot["coords"])
                self.assertIn("lng", lot["coords"])

    @ddt.data(*get_tests())
    def test_city(self, city_name):
        self.sanity_check(city_name, scrape_city(city_name))

