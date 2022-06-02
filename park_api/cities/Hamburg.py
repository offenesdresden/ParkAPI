from bs4 import BeautifulSoup
import utm
from park_api.geodata import GeoData

geodata = GeoData(__file__)

def parse_html(xml):
    soup = BeautifulSoup(xml, "html.parser")

    data = {
        "lots": [],
        "last_updated": soup.find('wfs:featurecollection')["timestamp"][:-1]
    }

    region = "Hamburg"
    forecast = False

    for member in soup.find('wfs:featurecollection').find_all('gml:featuremember'):
        name = member.find('de.hh.up:name').string
        count = 0
        try:
            count = int(member.find('de.hh.up:stellplaetze_gesamt').string)
        except AttributeError:
            pass
        free = 0
        state = "nodata"
        situation = member.find('de.hh.up:situation')
        if situation and situation.string != "keine Auslastungsdaten":
            free = int(member.find('de.hh.up:frei').string)
            status = member.find('de.hh.up:status').string
            if status == "frei" or status == "besetzt":
                state = "open"
            else:
                state = "closed"
        lot_type = member.find('de.hh.up:art').string
        if lot_type == "Straßenrand":
            lot_type = "Parkplatz"
        lot_id = member.find('de.hh.up:id').string
        address = ""
        try:
            address = member.find('de.hh.up:einfahrt').string
        except AttributeError:
            try:
                address = member.find('de.hh.up:strasse').string
                try:
                    address += " " + member.find('de.hh.up:hausnr').string
                except (AttributeError, TypeError):
                    pass
            except AttributeError:
                pass

        coord_member = member.find('gml:pos')
        if coord_member:
            coord_string = coord_member.string.split()
            latlon = utm.to_latlon(float(coord_string[0]), float(coord_string[1]), 32, 'U')
            coords = {
                "lat": latlon[0],
                "lng": latlon[1]
            }
        else:
            coords = None
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
