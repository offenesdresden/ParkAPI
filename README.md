## ParkAPI

ParkAPI is a small project trying to consolidate pages where cities publish the amount of empty spaces on their public parking lots (albeit as HTML) into a simple to use JSON API. It's trying to become the new backend for ParkenDD ([iOS](https://github.com/kiliankoe/ParkenDD) & [Android](https://github.com/jklmnn/ParkenDD)).

Currently it's just a tiny python flask powered server and definitely nowhere near ready for actual usage. 

The idea here is to also include some more fun features like automatic time-based scraping and caching those results for quicker responses and reduced load on the servers providing data or providing forecast data right alongside.

### Schema

The current schema for the output looks something like this:

```js
{
  "last_changed": "Mon, 15 Jun 2015 12:31:00 GMT",
  "time_updated": "Mon, 15 Jun 2015 12:31:25 GMT",
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

Besides `name` and `free` all other attributes for a single lot are optional and might not exist for each city.

The top level params for when the data was last changed on the server and when it was pulled by the scraper should always be there.
