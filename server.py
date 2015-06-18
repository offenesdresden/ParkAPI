from flask import Flask, jsonify, json
from datetime import datetime, timedelta
from os import getloadavg
import scraper
import os
import configparser

app = Flask(__name__)

config = configparser.ConfigParser()
config.read("config.ini")

@app.route("/cities")
def get_city_list():
    return jsonify({
        "supported_cities": [
            "Dresden",
            "Ingolstadt",
            "Luebeck"
        ]
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
    try:
        file = open("./cache/" + city + ".json", "r")
        last_json = file.read()
        last_json = json.loads(last_json)
        last_downloaded = datetime.strptime(last_json["last_downloaded"], "%Y-%m-%d %H:%M:%S")
        if datetime.now() - last_downloaded <= timedelta(minutes=5):
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

if __name__ == "__main__":
    if os.getenv("env") == "development":
        app.run(debug=True)
    else:
        app.run(host=config["Server"]["host"], port=int(config["Server"]["port"]))
