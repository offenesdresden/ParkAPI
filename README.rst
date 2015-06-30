ParkAPI
=======

|Build Status|

ParkAPI is a small project trying to consolidate pages where cities
publish the amount of empty spaces on their public parking lots (albeit
as HTML) into a simple to use JSON API. It’s trying to become the new
backend for ParkenDD (`iOS`_ & `Android`_).

Currently it’s just a tiny python flask powered server and **definitely
nowhere near ready for actual usage**.

The idea here is to also include some more fun features like automatic
time-based scraping and caching those results for quicker responses and
reduced load on the servers providing data or providing forecast data
right alongside.

Usage
-----

For every city listed in ``park_api/cities`` or that’s returned when you send
the request below on the server you can GET ``server.tld/city_id`` to
receive a JSON response following the schema below.

**GET /**

.. code:: js

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

API version specifies the version of the JSON response whereas the
server version correlates to the version of the software in this repo.

You can use the server running at `park-api.higgsboson.tk`_ for testing.
It should usually be running at the most current version of this repo.

Setup your own server
---------------------

- First you will need python (at least 3.3), pip and virtualenv installed.
  In the following section it is assumed, that python is python3 and
  virtualenv is virtualenv3. If this is not the case for your distribution use
  the correct executables.

- Clone the repo::

  $ git clone git@github.com:offenesdresden/ParkAPI.git
  $ cd ParkAPI

- Create a new virtualenv::

  $ virtualenv venv
  $ . venv/bin/activate

- Install dependencies::

  (venv) $ pip install -e .

- Run the server::

  $ bin/parkapi-server

- Run the tests::

  $ python -m unittest discover tests

Schema
------

The schema for the output looks like this:

**GET /city\_id**

.. code:: js

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

Times are in UTC and parameters marked as optional may not exist.
Usually only when a city supplies this somehow and we can include it.

Also please note that this is not valid JSON. Just an example for how
the output can be expected. For a specific `JSON schema`_ please have a
look at the `wiki here`_.

Adding support for a new city
-----------------------------

You know of a city that publishes their current parking data but isn’t
yet supported by this project? Or you want to help out with one of the
cities listed `here`_? Awesome! Let’s get you started.

Just fork this project and go ahead and duplicate
``park_api/cities/Sample_City.py`` as a place to get started. A

.. _iOS: https://github.com/kiliankoe/ParkenDD
.. _Android: https://github.com/jklmnn/ParkenDD
.. _park-api.higgsboson.tk: https://park-api.higgsboson.tk
.. _JSON schema: http://json-schema.org
.. _wiki here: https://github.com/offenesdresden/ParkAPI/wiki/city.json
.. _here: https://github.com/offenesdresden/ParkAPI/issues?q=is%3Aopen+is%3Aissue+label%3Anew_data

.. |Build Status| image:: https://travis-ci.org/offenesdresden/ParkAPI.svg?branch=master
   :target: https://travis-ci.org/offenesdresden/ParkAPI
