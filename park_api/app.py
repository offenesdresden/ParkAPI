from datetime import datetime
from os import getloadavg
from flask import Flask, jsonify, abort, request

from park_api import scraper, util, env
from park_api.forecast import find_forecast
from park_api.crossdomain import crossdomain

app = Flask(__name__)


@app.route("/")
@crossdomain("*")
def get_meta():
    cities = {}
    for module in env.supported_cities().values():
        city = module.geodata.city
        cities[city.id] = city.as_json()
    return jsonify({
        "cities": cities,
        "api_version": env.API_VERSION,
        "server_version": env.SERVER_VERSION,
        "reference": env.SOURCE_REPOSITORY
    })


@app.route("/status")
@crossdomain("*")
def get_api_status():
    return jsonify({
        "status": "online",
        "server_time": util.utc_now(),
        "load": getloadavg()
    })


@app.route("/<city>")
@crossdomain("*")
def get_lots(city):
    if city == "favicon.ico" or city == "robots.txt":
        abort(404)

    city_module = env.supported_cities().get(city, None)

    if city_module is None:
        app.logger.info("Unsupported city: " + city)
        return ("Error 404: Sorry, '" +
                city +
                "' isn't supported at the current time.", 404)

    if env.LIVE_SCRAPE:
        lots = scraper.scrape(city_module)
        return jsonify(lots.as_json())

    lots = city_module.geodata.lots
    lots.load()

    return jsonify(lots.as_json())


@app.route("/<city>/<lot_id>/timespan")
@crossdomain("*")
def get_longtime_forecast(city, lot_id):
    try:
        datetime.strptime(request.args["from"], '%Y-%m-%dT%H:%M:%S')
        datetime.strptime(request.args["to"], '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        return ("Error 400: from and/or to URL params "
                "are not in ISO format, e.g. 2015-06-26T18:00:00", 400)

    data = find_forecast(lot_id, request.args["from"], request.args["to"])
    if data is not None:
        return jsonify(data)
    else:
        abort(404)


@app.route("/coffee")
def make_coffee():
    return """
    <h1>I'm a teapot</h1>
    <p>This server is a teapot, not a coffee machine.</p><br>
    <img src="http://i.imgur.com/xVpIC9N.gif"
         alt="British porn"
         title="British porn"/>
    """, 418


@app.before_request
def log_request():
    ua = request.headers.get("User-Agent")
    if not ua:
        ua = "no user-agent"
    app.logger.info("%s %s - %s" % (request.method, request.path, ua))
