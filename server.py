from flask import Flask, jsonify, json, abort, request
from datetime import datetime, timedelta
from os import getloadavg
import scraper
import os
import configparser
import logging
from logging.handlers import RotatingFileHandler
import util
import structs
from security import file_is_allowed
import api_conf
import importlib
from forecast import find_forecast
import psycopg2

app = Flask(__name__)

SUPPORTED_CITIES = {}

if os.getenv("env") != "development":

    config = configparser.ConfigParser()
    config.read("config.ini")

    raw_server_conf = config["Server"]

    try:
        used_port = int(raw_server_conf.get('port', api_conf.DEFAULT_SERVER.port))
    except ValueError:
        used_port = api_conf.DEFAULT_SERVER.port

    SERVER_CONF = structs.ServerConf(
        host=raw_server_conf.get('host', api_conf.DEFAULT_SERVER.host),
        port=used_port,
    )

    db_data = {
        "host": config["Database"]["host"],
        "name": config["Database"]["name"],
        "user": config["Database"]["user"],
        "pass": config["Database"]["pass"],
        "port": config["Database"]["port"]
    }

    del raw_server_conf, used_port, config
else:
    SERVER_CONF = api_conf.DEFAULT_SERVER


@app.route("/")
def get_meta():
    app.logger.info("GET / - " + request.headers.get("User-Agent"))

    return jsonify({
        "cities": SUPPORTED_CITIES,
        "api_version": api_conf.API_VERSION,
        "server_version": api_conf.SERVER_VERSION,
        "reference": api_conf.SOURCE_REPOSITORY
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

    if city not in SUPPORTED_CITIES:
        app.logger.info("Unsupported city: " + city)
        return "Error 404: Sorry, '" + city + "' isn't supported at the current time.", 404

    if os.getenv("env") == "development":
        return jsonify(scraper._live(city))

    try:
        with psycopg2.connect(database=db_data["name"], user=db_data["user"], host=db_data["host"], port=db_data["port"],
                              password=db_data["pass"]) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT timestamp_updated, timestamp_downloaded, data FROM parkapi_test WHERE city=%s;", (city,))
            data = cursor.fetchall()[-1][2]
    except psycopg2.OperationalError:
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


def gather_supported_cities():
    """
    Iterate over files in ./cities to add them to list of available cities.
    This list is used to stop requests trying to access files and output them which are not cities.
    """
    cities = {}
    for file in filter(file_is_allowed, os.listdir(os.path.join(os.curdir, "cities"))):
        city = importlib.import_module("cities." + file.title()[:-3])
        cities[file[:-3]] = city.city_name
    return cities


if __name__ == "__main__":
    log_handler = RotatingFileHandler("server.log", maxBytes=1000000, backupCount=1)
    log_handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s "
    ))

    SUPPORTED_CITIES = gather_supported_cities()

    if os.getenv("env") == "development":
        app.logger.addHandler(log_handler)

        app.run(debug=True)
    else:
        app.logger.setLevel(logging.INFO)
        log_handler.setLevel(logging.INFO)
        app.logger.addHandler(log_handler)

        app.run(host=SERVER_CONF.host, port=SERVER_CONF.port)
