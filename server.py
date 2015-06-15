from flask import Flask, jsonify
from cities import Ingolstadt, Dresden
app = Flask(__name__)

@app.route("/<city>/")
def get_lots(city):
    if city == "Ingolstadt":
        return jsonify(Ingolstadt.get_data())
    elif city == "Dresden":
        return jsonify(Dresden.get_data())

@app.route("/<city>/<lot_id>")
def get_lot_details(city, lot_id):
    if city == "Dresden":
        return Dresden.get_lot_details(lot_id)

if __name__ == "__main__":
    app.run(debug=True)
