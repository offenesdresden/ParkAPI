from flask import Flask, jsonify
from datetime import datetime
from os import getloadavg
import scraper

app = Flask(__name__)

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
    return jsonify(scraper.live(city))

# @app.route("/<city>/<lot_id>")
# def get_lot_details(city, lot_id):
#     if city == "Dresden":
#         return Dresden.get_lot_details(lot_id)

if __name__ == "__main__":
    app.run(debug=True)
