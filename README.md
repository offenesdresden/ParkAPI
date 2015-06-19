## ParkAPI

ParkAPI is a small project trying to consolidate pages where cities publish the amount of empty spaces on their public parking lots (albeit as HTML) into a simple to use JSON API. It's trying to become the new backend for ParkenDD ([iOS](https://github.com/kiliankoe/ParkenDD) & [Android](https://github.com/jklmnn/ParkenDD)).

Currently it's just a tiny python flask powered server and **definitely nowhere near ready for actual usage**. 

The idea here is to also include some more fun features like automatic time-based scraping and caching those results for quicker responses and reduced load on the servers providing data or providing forecast data right alongside.

### Usage

For every city listed in `/cities` or that's returned when you GET `/cities` on the server you can GET `server.tld/city_name` to receive a JSON response following the schema below.

You can use the server running at [parkendd.higgsboson.tk](http://parkendd.higgsboson.tk) for testing. It should usually be running at the most current version of this repo.

### Schema

The current (not final!) schema for the output looks something like this:

```js
{
  "last_changed": "Mon, 15 Jun 2015 12:31:00 GMT",
  "last_downloaded": "Mon, 15 Jun 2015 12:31:25 GMT",
  "lots": [
    {
      "coords": {
        "lat": 51.05031,
        "lon": 13.73754
      },
      "count": 400,
      "free": 235,
      "id": "TG16",
      "name": "Altmarkt",
      "state": "many"
    },
    [...]
}
```

Besides `name` all other attributes for a single lot are optional and might not exist for each city.

The top level params for when the data was last changed on the server and when it was pulled by the scraper should always be there.

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