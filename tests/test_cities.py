import os
import unittest
import helpers
import importlib


def scrape_city(city, extension=".html"):
    path = os.path.join(helpers.TEST_ROOT, "fixtures", city.lower() + extension)
    with open(path) as f:
        city = importlib.import_module("cities." + city)
        city.parse_html(f.read())


class CityTestCase(unittest.TestCase):
    def test_dresden(self):
        scrape_city("Dresden")

    def test_ingolstadt(self):
        scrape_city("Ingolstadt")

    def test_konstanz(self):
        scrape_city("Konstanz")

    def test_luebeck(self):
        scrape_city("Luebeck")

    def test_zuerich(self):
        scrape_city("Zuerich", ".xml")

    def test_muenster(self):
        scrape_city("Muenster")
