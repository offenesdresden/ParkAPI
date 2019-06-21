#!/usr/bin/env python3

import sys
import json

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        data = json.load(f)

    geo = {"type":"FeatureCollection",
           "features":[{
               "type":"Feature",
               "geometry":{
                   "type":"Point",
                   "coordinates":[
                       6.958249,
                       50.941387
                   ]
               },
               "properties":{
                   "name":"Köln",
                   "type":"city",
                   "url":"https://offenedaten-koeln.de/dataset/parkhausbelegung",
                   "source":"https://www.stadt-koeln.de/externe-dienste/open-data/parking-ts.php",
                   "active_support":False
                }
            }
        ]
    }

    for k in data.keys():
        aux = {"identifier":k,
               "open":data[k]["open"] == "durchgehend"}
        geo["features"].append({
            "type":"Feature",
            "properties":{
                "name":data[k]["title"].replace(" (*)", ""),
                "total":int(data[k]["capacity"]),
                "address":data[k]["street"] + " " + data[k]["housenumber"],
                "type":"Parkhaus",
                "aux":json.dumps(aux)
            },
            "geometry":{
                "type":"Point",
                "coordinates":[
                    float(data[k]["lng"]),
                    float(data[k]["lat"])
                ]
            }
        })

    with open("Koeln.geojson", "w") as geojson:
        json.dump(geo, geojson, indent=4, sort_keys=True, ensure_ascii=False)

