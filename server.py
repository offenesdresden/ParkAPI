from flask import Flask, jsonify
from cities import Ingolstadt
app = Flask(__name__)

@app.route("/<city>/")
def hello(city):
    if city == "Ingolstadt":
        return jsonify(Ingolstadt.get_data())

if __name__ == "__main__":
    app.run()
