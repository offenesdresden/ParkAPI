from flask import Flask, jsonify, json
from cities import Ingolstadt, Dresden
app = Flask(__name__)

@app.route("/<city>/")
def hello(city):
    if city == "Ingolstadt":
        return jsonify(Ingolstadt.get_data())
    elif city == "Dresden":
        return json.dumps(Dresden.get_data())

if __name__ == "__main__":
    app.run(debug=True)
