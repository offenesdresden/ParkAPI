from bs4 import BeautifulSoup
import utm
from park_api.geodata import GeoData

geodata = GeoData(__file__)

def parse_html(xml):
    soup = BeautifulSoup(xml, "html.parser")
    
    data = {
        "lots": [],
        "last_updated": soup.find('wfs:featurecollection')['timestamp'][:-1]
    }
    
    region = "Hamburg"
    forecast = False
    
    for member in soup.find('wfs:featurecollection').find_all('gml:featuremember'):
        name = member.find('app:name').string
        count = 0
        try:
            count = int(member.find('app:stellplaetze_gesamt').string)
        except AttributeError:
            pass
        free = 0
        state = "nodata"
        if member.find('app:situation').string != "keine Auslastungsdaten":
            free = int(member.find('app:frei').string)
            status = member.find('app:status').string
            if status == "frei" or status == "besetzt":
                state = "open"
            else:
                state = "closed"
        lot_type = member.find('app:art').string
        if lot_type == "Straßenrand":
            lot_type = "Parkplatz"
        lot_id = member.find('app:id').string
        address = ""
        try:
            address = member.find('app:einfahrt').string
        except AttributeError:
            try:
                address = member.find('app:strasse').string
                try:
                    address += " " + member.find('app:hausnr').string
                except AttributeError:
                    pass
            except AttributeError:
                pass
        coord_string = member.find('gml:pos').string.split()
        latlon = utm.to_latlon(float(coord_string[0]), float(coord_string[1]), 32, 'U')
        coords = {
            "lat": latlon[0],
            "lng": latlon[1]
        }
        data['lots'].append({
           "coords":coords,
           "name":name,
           "id": lot_id,
           "lot_type": lot_type,
           "total":count,
           "free":free,
           "state":state,
           "region":region,
           "forecast":forecast,
           "address":address
        })
       
    return data