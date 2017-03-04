import os
import unittest
import helpers
import importlib
from datetime import datetime
from park_api import db


def scrape_city(city, extension=".html"):
    path = os.path.join(helpers.TEST_ROOT,
                        "fixtures",
                        city.lower() + extension)
    with open(path, 'rb') as f:
        city = importlib.import_module("park_api.cities." + city)
        return city.parse_html(f.read().decode('utf-8', 'replace'))


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

    def test_dresden(self):
        city_name = "Dresden"
        self.sanity_check(city_name, scrape_city(city_name))

    def test_ingolstadt(self):
        city_name = "Ingolstadt"
        self.sanity_check(city_name, scrape_city(city_name))

    def test_konstanz(self):
        city_name = "Konstanz"
        self.sanity_check(city_name, scrape_city(city_name))

    def test_luebeck(self):
        city_name = "Luebeck"
        self.sanity_check(city_name, scrape_city(city_name))

    def test_zuerich(self):
        city_name = "Zuerich"
        self.sanity_check(city_name, scrape_city(city_name, ".xml"))

    def test_muenster(self):
        city_name = "Muenster"
        self.sanity_check(city_name, scrape_city(city_name))

    def test_bonn(self):
        city_name = "Bonn"
        self.sanity_check(city_name, scrape_city(city_name))

    def test_oldenburg(self):
        city_name = "Oldenburg"
        self.sanity_check(city_name, scrape_city(city_name))
    
    def test_hamburg(self):
        city_name = "Hamburg"
        self.sanity_check(city_name, scrape_city(city_name, ".xml"))

    def test_freiburg(self):
        city_name = "Freiburg"
        self.sanity_check(city_name, scrape_city(city_name, ".json"))

    def test_aarhus(self):
        city_name = "Aarhus"
        self.sanity_check(city_name, scrape_city(city_name, ".json"))

    def test_odense(self):
        city_name = "Odense"
        self.sanity_check(city_name, scrape_city(city_name, ".json"))

    def test_aalborg(self):
        city_name = "Aalborg"
        self.sanity_check(city_name, scrape_city(city_name, ".json"))

    def test_sample(self):
        city_name = "Sample_City"
        self.sanity_check(city_name, scrape_city(city_name))

    def test_frankfurt(self):
        city_name = "Frankfurt"
        self.sanity_check(city_name, scrape_city(city_name, ".xml"))
