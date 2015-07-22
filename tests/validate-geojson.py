#!/usr/bin/env python
import sys, os
import json

def validate_geometry(geometry):
   _type = geometry.get("type", None)
   assert _type == "Point", \
       "geometry should contain a key with the value 'Point', got: '%s'" % _type
   coords = geometry.get("coordinates", None)
   assert type(coords) is list and len(coords) == 2 and \
       type(coords[0]) == float and type(coords[1]) == float, \
       "invalid coordinates: got '%s' in '%s'" % (coords, geometry)


def validate_feature(feature):
   assert type(feature) == dict, \
       "each entry of array 'features' " \
       "should be an object, got: '%s'" % feature

   _type = feature.get("type", None)
   assert _type == "Feature", \
       "each entry of array 'features' should contain the key 'type' with value 'Feature', got: '%s'" % _type

   assert "geometry" in feature, \
       "each entry of array 'features' should contain the key 'geometry', got: '%s'" % feature

   geometry = feature.get("geometry", None)

   if type(geometry) is dict:
       validate_geometry(geometry)
   elif geometry != None:
       assert False, "geometry must be null or object got: '%s' in '%s'" % (geometry, feature)

   prop = feature.get("properties", None)
   assert type(prop) is dict, \
       "properties must be an object, got: '%s' in '%s'" % (prop, feature)
   assert "name"  in prop, \
           "properties must contain a 'name' key, got: '%s' in %s" % (prop, feature)



def validate_schema(geojson):
    assert type(geojson) is dict, "Toplevel object should be an JSON object"
    assert geojson.get("type", None) == "FeatureCollection", \
        "Toplevel object should contain a key 'type' with value 'FeatureCollection'"
    assert type(geojson.get("features", None)) == list, \
        "Toplevel object should contain a key 'features', where the type is an array"
    for feature in geojson["features"]:
        validate_feature(feature)


def process_json(path):
   try:
       file = open(path)
   except OSError as e:
       print("failed to open '%s': %s" % (path, e), file=sys.stderr)
       sys.exit(1)
   validate_schema(json.load(file))


def main():
    if len(sys.argv) <= 1:
        print("USAGE: %s GEOJSON_FILES..." % sys.argv[0], file=sys.stderr)
        sys.exit(1)
    for path in sys.argv[1:]:
        process_json(path)


if __name__ == '__main__':
    main()
