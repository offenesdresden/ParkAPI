GEOJSON=swift run geojson

build:
	$(GEOJSON)
	swift build

test:
	$(GEOJSON)
	swift test --parallel

.PHONY: build, test
