from flask import Flask, jsonify
from cities import Ingolstadt, Dresden
app = Flask(__name__)

@app.route("/<city>/")
def hello(city):
    if city == "Ingolstadt":
        return jsonify(Ingolstadt.get_data())
    elif city == "Dresden":
        return jsonify(Dresden.get_data())

if __name__ == "__main__":
    app.run(debug=True)
