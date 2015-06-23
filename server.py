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


app = Flask(__name__)


SUPPORTED_CITIES = []



if os.getenv("env") != "development":

    config = configparser.ConfigParser()
    config.read("config.ini")

    raw_server_conf = config.get('server', {})

    try:
        used_port = int(raw_server_conf.get('port', api_conf.DEFAULT_SERVER.port))
    except ValueError:
        used_port = api_conf.DEFAULT_SERVER.port

    SERVER_CONF = structs.ServerConf(
        host = raw_server_conf.get('host', api_conf.DEFAULT_SERVER.host),
        port = used_port,
        mail = raw_server_conf.get('mail', api_conf.DEFAULT_SERVER.mail)
    )

    # cleaning temporary variables
    del raw_server_conf, used_port, config
else:
    SERVER_CONF = structs.ServerConf(
        host=api_conf.DEFAULT_SERVER.host,
        port=api_conf.DEFAULT_SERVER.port,
        mail=api_conf.DEFAULT_SERVER.mail
    )


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
        return jsonify({
                "error": "Sorry, '" + city + "' isn't supported at the current time."
            }), 404
    try:
        with open("./cache/" + city + ".json", "r") as file:
            last_json = json.load(file)
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
