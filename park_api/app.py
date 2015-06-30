from datetime import datetime
from os import getloadavg

from flask import Flask, jsonify, abort, request
import psycopg2
from park_api import scraper, util, env
from park_api.forecast import find_forecast

app = Flask(__name__)


@app.route("/")
def get_meta():
    app.logger.info("GET / - " + request.headers.get("User-Agent"))

    cities = {}
    for city_id, city in env.supported_cities().items():
        cities[city.city_name] = city_id

    return jsonify({
        "cities": cities,
        "api_version": env.API_VERSION,
        "server_version": env.SERVER_VERSION,
        "reference": env.SOURCE_REPOSITORY
    })


@app.route("/status")
def get_api_status():
    return jsonify({
        "status": "online",
        "server_time": util.utc_now(),
        "load": getloadavg()
    })


@app.route("/<city>")
def get_lots(city):
    if city == "favicon.ico" or city == "robots.txt":
        abort(404)

    app.logger.info("GET /" + city + " - " + request.headers.get("User-Agent"))

    city_module = env.supported_cities().get(city, None)

    if city_module is None:
        app.logger.info("Unsupported city: " + city)
        return "Error 404: Sorry, '" + city + "' isn't supported at the current time.", 404

    if env.LIVE_SCRAPE:
        return jsonify(scraper._live(city_module))

    try:
        with psycopg2.connect(**env.DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT timestamp_updated, timestamp_downloaded, data FROM parkapi WHERE city=%s;", (city,))
            data = cursor.fetchall()[-1][2]
    except (psycopg2.OperationalError, psycopg2.ProgrammingError) as e:
        app.logger.error("Unable to connect to database: " + str(e))
        abort(500)

    return jsonify(data)


@app.route("/<city>/<lot_id>/timespan")
def get_longtime_forecast(city, lot_id):
    app.logger.info("GET /" + city + "/" + lot_id + "/timespan - " + request.headers.get("User-Agent"))

    try:
        datetime.strptime(request.args["from"], '%Y-%m-%dT%H:%M:%S')
        datetime.strptime(request.args["to"], '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        return "Error 400: from and/or to URL params are not in ISO format, e.g. 2015-06-26T18:00:00", 400

    data = find_forecast(lot_id, request.args["from"], request.args["to"])
    if data is not None:
        return jsonify(data)
    else:
        abort(404)


@app.route("/coffee")
def make_coffee():
    app.logger.info("GET /coffee - " + request.headers.get("User-Agent"))

    return "<h1>I'm a teapot</h1>" \
           "<p>This server is a teapot, not a coffee machine.</p><br>" \
           "<img src=\"http://i.imgur.com/xVpIC9N.gif\" alt=\"British porn\" title=\"British porn\">", 418
