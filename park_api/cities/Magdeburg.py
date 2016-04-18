from bs4 import BeautifulSoup
from park_api.geodata import GeoData

geodata = GeoData(__file__)

def parse_html(html):
  
  soup = BeautifulSoup(html, "html.parser")
  
  lots = []
  tds = soup.find_all("td")
  for i, entry in enumerate(tds):
    lot = {}
    try:
      if entry.font.a['style'] == "color:blue; text-decoration:underline": 
        lot['name'] = entry.font.a.string
        print(entry.font.a.string)
        print(tds[i+1].font.strong.string)
    except (AttributeError, TypeError):
      pass