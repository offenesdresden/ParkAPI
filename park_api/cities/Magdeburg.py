from bs4 import BeautifulSoup
from park_api.geodata import GeoData
from datetime import datetime
from park_api.util import convert_date

geodata = GeoData(__file__)

def parse_html(html):
  
  soup = BeautifulSoup(html, "html.parser")
  
  lots = []
  dates = []
  tds = list(enumerate(soup.find_all("td")))
  for i, entry in tds:
    try:
      if entry.font.a['style'] == "color:blue; text-decoration:underline":
        name = entry.font.a.string
        lot = geodata.lot(name)
        free = 0
        state = "unknown"
        fs = tds[i+1][1].font.strong.string
        try:
          dates.append(datetime.strptime(tds[i+4][1].font.strong.string.strip(), "%d.%m.%Y %H:%M Uhr"))
        except (AttributeError, TypeError, ValueError) as e:
          pass
        try:
          free = int(fs)
        except ValueError:
          state = "closed"
        lots.append({
          "coords": None,
          "name": name,
          "total": lot.total,
          "free": free,
          "state": state,
          "id": lot.id,
          "lot_type": lot.type,
          "address": None,
          "forecast": False,
          "region": None
        })
    except (AttributeError, TypeError):
      pass
  
  dates.sort()
  dates = list(reversed(dates))
    
  return {
    "last_updated":convert_date(dates[0].strftime("%d.%m.%Y %H:%M"), "%d.%m.%Y %H:%M"),
    "lots":lots
  }