from flask import Flask, jsonify, json, abort, request
from datetime import datetime, timedelta
from os import getloadavg
import scraper
import os
import configparser
import logging
from logging.handlers import RotatingFileHandler
from collections import namedtuple


app = Flask(__name__)


ServerConf = namedtuple('ServerConf', ['port', 'host', 'mail'])


DEFAULTS = ServerConf(
    port = 5000,
    host = 'localhost',
    mail = ''
)
SUPPORTED_CITIES = []



if os.getenv("env") != "development":

    config = configparser.ConfigParser()
    config.read("config.ini")

    raw_server_conf = config.get('server', {})

    try:
        used_port = int(raw_server_conf.get('port', DEFAULTS.port))
    except ValueError:
        used_port = DEFAULTS.port

    SERVER_CONF = ServerConf(
        host = raw_server_conf.get('host', DEFAULTS.host),
        port = used_port,
        mail = raw_server_conf.get('mail', DEFAULTS.mail)
    )

    # cleaning temporary variables
    del raw_server_conf, used_port, config


@app.route("/")
def get_meta():
    return jsonify({
        "mail": SERVER_CONF.mail,
        "cities": SUPPORTED_CITIES
    })


@app.route("/status")
def get_api_status():
    return jsonify({
        "status": "online",
        "server_time": datetime.utcnow().replace(microsecond=0).isoformat(),
        "load": getloadavg()
    })


@app.route("/<city>")
def get_lots(city):
    if city == "favicon.ico" or city == "robots.txt":
        abort(404)

    app.logger.info("GET /" + city + " - " + request.headers.get("User-Agent"))

    if city not in SUPPORTED_CITIES:
        app.logger.info("Unsupported city: " + city)
        return jsonify({
            "error": "Sorry, '" + city + "' isn't supported at the current time."
        }), 404
    try:
        file = open("./cache/" + city + ".json", "r")
        last_json = file.read()
        last_json = json.loads(last_json)
        last_downloaded = datetime.strptime(last_json["last_downloaded"], "%Y-%m-%dT%H:%M:%S")
        if datetime.utcnow() - last_downloaded <= timedelta(minutes=10):
            app.logger.debug("Using cached data")
            return jsonify(last_json)
        else:
            return jsonify(scraper.live(city))
    except FileNotFoundError:
        return jsonify(scraper.live(city))


@app.route("/coffee")
def make_coffee():
    return "<h1>I'm a teapot</h1>" \
           "<p>This server is a teapot, not a coffee machine.</p><br>" \
           "<img src=\"http://i.imgur.com/xVpIC9N.gif\" alt=\"British porn\" title=\"British porn\">", 418


def file_is_allowed(file):
    return file.endswith(".py") and "__Init__" not in file.title() and "Sample_City" not in file.title()


def gather_supported_cities():
    """
    Iterate over files in ./cities to add them to list of available cities.
    This list is used to stop requests trying to access files and output them which are not cities.
    """
    return [

        file[:-3]

        for file in
            filter(file_is_allowed, os.listdir(os.curdir + "/cities"))
    ]


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
