GEOJSON=swift run geojson

read-geojson:
	$(GEOJSON)

build: read-geojson
	swift build

test: read-geojson
	swift test

test-live: read-geojson
	export TEST_LIVE=1;\
	swift test

.PHONY: read-geojson, build, test, test-live
