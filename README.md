## ParkAPI

[![Build Status](https://travis-ci.org/offenesdresden/ParkAPI.svg?branch=master)](https://travis-ci.org/offenesdresden/ParkAPI)

ParkAPI is a small project trying to consolidate pages where cities publish the amount of empty spaces on their public parking lots (albeit as HTML) into a simple to use JSON API. It's trying to become the new backend for ParkenDD ([iOS](https://github.com/kiliankoe/ParkenDD) & [Android](https://github.com/jklmnn/ParkenDD)).

Currently it's just a tiny python flask powered server and **definitely nowhere near ready for actual usage**. 

The idea here is to also include some more fun features like automatic time-based scraping and caching those results for quicker responses and reduced load on the servers providing data or providing forecast data right alongside.

### Usage

For every city listed in `/cities` or that's returned when you send the request below on the server you can GET `server.tld/city_id` to receive a JSON response following the schema below.

**GET /**

```js
{
    "api_version": "1.0",
    "server_version": "1.0.0",
    "reference": "https://github.com/offenesdresden/ParkAPI",
    "cities":
        {
        	"city1id": "City 1",
         	"city2id": "City 2",
         	...
        }
}
```

API version specifies the version of the JSON response whereas the server version correlates to the version of the software in this repo.

You can use the server running at [park-api.higgsboson.tk](https://park-api.higgsboson.tk) for testing. It should usually be running at the most current version of this repo.

### Schema

The schema for the output looks like this:

**GET /city_id**

```js
{
  "last_updated": "2015-06-15T12:31:00",
  "last_downloaded": "2015-06-15T12:31:25",
  "data_source": "http://examplecity.com",
  "lots": [
    {
      "coords": {
        "lat": 51.05031,
        "lng": 13.73754
      },
      "name": "Altmarkt",
      "total": 400,
      "free": 235,
      "state": "open|closed|nodata",
      "id": "lot_id",
      "forecast": true|false,
      "region": "Region X", // optional
      "address": "Musterstraße 5", // optional
      "lot_type": "Parkhaus" // optional
    },
    ...
}
```

Times are in UTC and parameters marked as optional may not exist. Usually only when a city supplies this somehow and we can include it.

Also please note that this is not valid JSON. Just an example for how the output can be expected. For a specific [JSON schema](http://json-schema.org) please have a look at the [wiki here](https://github.com/offenesdresden/ParkAPI/wiki/city.json).

### Adding support for a new city

Have a look at `cities/Sample_City.py` as a place to get started and the other city scrapers for reference. The basic idea is to include all code specific to gathering data for a city in its file.

If you have the necessary geodata it'd be great if you could create a geojson file as well. It's name is the same as the city and in the same directory, just with `.geojson` at the end.
[geojson.io](http://geojson.io) is definitely a recommended ressource as well!

When you're done include it in the tests and see if it all works out.

Awesome! Thanks for helping out!

*Note*: Please don't include umlauts or other special characters in the name of the city file(s). The correct city name is specified inside the `city.py` file, but the filename should be ascii-compatible.

### Installation

To get this running locally you'll need Python 3.x and pip installed. First install the dependencies (1) and then duplicate (2) and fill in the config file if you wish to run on a custom host and port. 

If you specify an environment variable `env` to `development` (3) the server runs in debug mode on localhost and port 5000 per default without needing the config file.

```bash
(1) $ pip install -r requirements.txt
(2) $ cp config_example.ini config.ini

(3) $ env=development
```

Then just start the server with

```bash
$ python server.py
```

Throwing errors? Sure you installed the requirements and are using Python 3.x? And you have specified a config file or set the environment variable? Still nothing? Please [tell us](https://github.com/offenesdresden/ParkAPI/issues/new) about it.