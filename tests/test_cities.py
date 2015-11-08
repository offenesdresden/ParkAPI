import os
import unittest
import helpers
import importlib
import glob
from datetime import datetime
from park_api import db, env


def scrape_city(city):
    pattern = os.path.join(helpers.TEST_ROOT,
                           "fixtures",
                           city.lower() + ".*")
    for path in glob.glob(pattern):
        with open(path, 'rb') as f:
            city = importlib.import_module("park_api.cities." + city)
            return city.parse_html(f.read().decode('utf-8', 'replace'))
    raise Exception("no test input file find for %s: %s" % (city, pattern))


class CityTestCase(unittest.TestCase):
    def setUp(self):
        db.setup()

    def sanity_check(self, city_name, lots):
        self.assertGreater(len(lots), 1)

        for lot in lots:
            self.assertIsInstance(lot.updated_at, datetime)
            self.assertIsInstance(lot.name, str)

            self.assertIn(lot.state,
                          ["open", "closed", "nodata", "unknown"])

            self.assertIsInstance(lot.free, int)
            self.assertIsInstance(lot.total, int)
            if lot.total < lot.free:
                msg = "\n[warn] total lots should be more than free lots:"\
                      " %d >= %d: %s => %s"
                print(msg % (lot.total, lot.free, city_name, lot))

for city in env.supported_cities().keys():
    def gen_test(city):
        def test(self):
            self.sanity_check(city, scrape_city(city))
        return test
    setattr(CityTestCase, "test_%s" % city.lower(), gen_test(city))
