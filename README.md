## ParkAPI

[![Build Status](https://travis-ci.org/offenesdresden/ParkAPI.svg?branch=master)](https://travis-ci.org/offenesdresden/ParkAPI)

ParkAPI is a project trying to consolidate pages where cities publish the amount of empty spaces on their public parking lots (be it an HTML page, XML data or something else) into a simple to use JSON API. This then serves as a backend for the mobile app ParkenDD ([iOS](https://github.com/kiliankoe/ParkenDD) & [Android](https://github.com/jklmnn/ParkenDD)).

**View the current data directly directly in your browser [here](https://offenesdresden.github.io/ParkAPI/).**

![image](./image.jpg)

The idea here is to fetch new data from the relevant pages regularly and serve that from the application so that the amount of stress on the original servers can be kept to a minimum. This data then also enables the calculation of forecast data (short- and longterm) that can be provided right alongside.

This software is currently running at [api.parkendd.de](https://api.parkendd.de). It should always be at the most current version of this repo.

### Usage

**GET /**

Get metadata containing the list of supported cities and their IDs (usually just the same name with replaced umlauts and no spaces), a link to this repository and both the version of the JSON output (`api_version`) and of the server application (`server_version`).

```js
{
    "api_version": "1.0",
    "server_version": "1.0.0",
    "reference": "https://github.com/offenesdresden/ParkAPI",
    "cities":
        {
            "City 1": "city1id",
            "City 2": "city2id",
            ...
        }
}
```

**GET /city\_id**

Get data for a single city that looks something like this. Times are in UTC and parameters marked as optional may not exist for each city or parking lot. Usually only when a city supplies this somehow and we can include it.

Also please note that this is not valid JSON. Just an example for how the output can be expected. For a specific [JSON schema](http://json-schema.org) please have a look at the [wiki here](https://github.com/offenesdresden/ParkAPI/wiki/city.json).


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
      "free": 235, // >= 0, optional, can be missing, if no live data available
      "state": "open|closed|nodata|unknown",
      "id": "lot_id",
      "forecast": true|false,
      "region": "Region X", // optional
      "address": "Musterstraße 5", // optional
      "lot_type": "Parkhaus", // optional,
      "opening_hours": "24/7", // optional, in OSM opening_hours syntax
      "fee_hours": "Mo-Fr 07:00-22:00; PH off", // optional, in OSM opening_hours syntax
      "url": "http://examplecity.com/parken/Altmarkt" // optional
    },
    ...
}
```


### Setup your own server

 - First you will need python (at least 3.7), pip and virtualenv installed. In the following it is assumed that python is python3 and virtualenv is virtualenv3. If this is not the case for your distribution please use the correct executables. If virtualenv3 is not available, use virtualenv -p /usr/bin/python3.
 
 - Install the following packages: postgresql libpq-dev

 - Clone the repo:

		$ git clone git@github.com:offenesdresden/ParkAPI.git
		$ cd ParkAPI

 - Create a new virtualenv:

        $ virtualenv venv
        $ source venv/bin/activate

 - Install dependencies:

        (venv) $ pip install -e .

 - Set up postgresql:

        $ sudo -u postgres createuser -P -d park_api  
        $ sudo -u postgres createdb -O park_api park_api

 - Run the server:

        $ bin/parkapi-server

 - Run the tests:

        $ python -m unittest discover tests
        
Throwing errors? Sure you installed the requirements and are using Python 3.x? Still nothing? Please [tell us](https://github.com/offenesdresden/ParkAPI/issues/new) about it.

### Adding support for a new city

You know of a city that publishes their current parking data but isn’t yet supported by this project? Or you want to help out with one of the cities listed [here](https://github.com/offenesdresden/ParkAPI/issues?q=is%3Aopen+is%3Aissue+label%3Anew_data)? Awesome! Let’s get you started.

Just fork this project and go ahead and duplicate `cities/Sample_City.py` as a place to get started. Also have a look at other city scrapers for reference. The basic idea is to include all code specific to gathering data for a city in its file.

If you have the necessary geodata it'd be great if you could create a geojson file as well. It's name is the same as the city and in the same directory, just with `.geojson` at the end.
[geojson.io](http://geojson.io) is definitely a recommended ressource as well!

When you're done don't forget to include your new city in the tests (`./tests/test_cities.py` - it's only three lines exactly identical to the other cities in there) and run them to see if it all works out.

Now all that's left to do is to send us a pull request with your new stuff :)

Very cool! Thanks for helping out! [You rock!](http://i.giphy.com/JVdF14CQQH7gs.gif)

*Note*: Please don't include umlauts or other special characters in the name of the city file(s). The correct city name is specified inside the `city.py` file, but the filename should be ascii-compatible and with underscores instead of spaces. Should a city with the same name already exist you're going to have to find some way to make it unique, maybe by including a state or region?

#### Credits

Image header by [Mattes](https://commons.wikimedia.org/wiki/User:Mattes) (Own work) [CC BY 2.0 de](http://creativecommons.org/licenses/by/2.0/de/deed.en), via Wikimedia Commons
