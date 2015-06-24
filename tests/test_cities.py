import os
import unittest
import helpers
import importlib
import datetime

def scrape_city(city, extension=".html"):
    path = os.path.join(helpers.TEST_ROOT, "fixtures", city.lower() + extension)
    with open(path, 'rb') as f:
        city = importlib.import_module("cities." + city)
        return city.parse_html(f.read().decode('utf-8', 'replace'))


class CityTestCase(unittest.TestCase):
    def sanity_check(self, city_name, city):
        self.assertIn("lots", city)
        self.assertIn("last_updated", city)
        last_updated = datetime.datetime.strptime(city["last_updated"], "%Y-%m-%dT%H:%M:%S")
        self.assertIsInstance(last_updated, datetime.datetime)

        for lot in city["lots"]:
            self.assertIn("name", lot)

            if "free" in lot and "count" in lot:
                count, free = lot["count"], lot["free"]
                if count < free:
                    msg = "\n[warn] lot count should be bigger then free lot count: %d >= %d: %s => %s"
                    print(msg %(count, free, city_name, lot))
            if "coords" in lot and lot["coords"] != []:
               self.assertIn("lat", lot["coords"])
               self.assertIn("lon", lot["coords"])
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
