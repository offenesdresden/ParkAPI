import os
import unittest
import helpers
import requests
import requests_mock
from park_api import env, scraper, db

class ScraperTestCase(unittest.TestCase):
    def setUp(self):
        db.setup()
    @requests_mock.Mocker()
    def test_insert(self, mock):
        path = os.path.join(helpers.TEST_ROOT, "fixtures", "dresden.html")
        cities = env.supported_cities()
        module = cities["Dresden"]
        with open(path) as f:
            src = module.geodata.city.source
            mock.get(src, text=f.read())
        scraper.scrape_city(module)
