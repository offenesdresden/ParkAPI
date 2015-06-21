from flask import Flask, jsonify, json, abort
from datetime import datetime, timedelta
from os import getloadavg
import scraper
import os
import configparser

app = Flask(__name__)

if os.getenv("env") is not "development":
    try:
        config = configparser.ConfigParser()
        config.read("config.ini")
        server_host = config["Server"]["host"]
        server_port = int(config["Server"]["port"])
        server_mail = config["Server"]["mail"]
    except (KeyError, ValueError):
        server_host = "localhost"
        server_port = 5000
        server_mail = ""

supported_cities = []


@app.route("/")
def get_meta():
    return jsonify({
        "mail": server_mail,
        "cities": supported_cities
    })


@app.route("/status")
def get_api_status():
    return jsonify({
        "status": "online",
        "servertime": datetime.now(),
        "load": getloadavg()
    })


@app.route("/<city>")
def get_lots(city):
    if city not in supported_cities:
        return jsonify({
            "error": "Sorry, '" + city + "' isn't supported at the current time."
        })
    try:
        file = open("./cache/" + city + ".json", "r")
        last_json = file.read()
        last_json = json.loads(last_json)
        last_downloaded = datetime.strptime(last_json["last_downloaded"], "%Y-%m-%d %H:%M:%S")
        if datetime.now() - last_downloaded <= timedelta(minutes=10):
            print("Using cached data, oh yeah!")
            return jsonify(last_json)
        else:
            return jsonify(scraper.live(city))
    except FileNotFoundError:
        return jsonify(scraper.live(city))


# @app.route("/<city>/<lot_id>")
# def get_lot_details(city, lot_id):
#     if city == "Dresden":
#         return Dresden.get_lot_details(lot_id)

@app.route("/coffee")
def make_coffee():
    abort(418)


def gather_supported_cities():
    """
    Iterate over files in ./cities to add them to list of available cities.
    This list is used to stop requests trying to access files and output them which are not cities.
    """
    for file in os.listdir(os.curdir + "/cities"):
        if file.endswith(".py") and "__Init__" not in file.title() and "Sample_City" not in file.title():
            supported_cities.append(file[:-3])


if __name__ == "__main__":
    if os.getenv("env") == "development":
        gather_supported_cities()
        app.run(debug=True)
    else:
        gather_supported_cities()
        app.run(host=server_host, port=server_port)
