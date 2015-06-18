from bs4 import BeautifulSoup

# The URL for the page where the parking lots are listed
data_url = "http://example.com"

# Name of the city, just in case it contains umlauts which this filename shouldn't
city_name = "Sample City"

# Name of this file (without '.py'), sorry for needing this, but it makes things easier
file_name = "Sample_City"

def parse_html(html):
    soup = BeautifulSoup(html)

    # Do everything necessary to scrape the contents of the html
    # into a dictionary of the format specified by the schema.
