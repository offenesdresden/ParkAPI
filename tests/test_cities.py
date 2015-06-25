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
        self.assertIn("data_source", city)
        last_updated = datetime.datetime.strptime(city["last_updated"], "%Y-%m-%dT%H:%M:%S")
        self.assertIsInstance(last_updated, datetime.datetime)

        for lot in city["lots"]:
            self.assertIn("name", lot)

            self.assertIn("coords", lot)

            self.assertIn("state", lot)
            self.assertRegex(lot["state"], "(open|closed|nodata)")

            self.assertIn("id", lot)

            self.assertIn("forecast", lot)
            self.assertIs(type(lot["forecast"]), bool)

            self.assertIn("free", lot)
            self.assertIn("total", lot)
            total, free = lot["total"], lot["free"]
            if total < free:
                msg = "\n[warn] total lots should be more than free lots: %d >= %d: %s => %s"
                print(msg % (total, free, city_name, lot))
            if "coords" in lot and lot["coords"] is not None:
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
