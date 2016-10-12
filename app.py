# -*- coding: utf-8 -*-

from flask import Flask


# create the Flask application
app = Flask(__name__)


@app.route("/cars", methods=["GET"])
def list_cars():
    return "Cars list will appear here"


@app.route("/car/<string:id>", methods=["GET"])
def car_by_id(id):
    abort(404)


@app.route("/car/<string:id>/price/<string:new_price>", methods=["PUT"])
def update_car_price(id, new_price):
    return "New price is" + new_price

if __name__ == "__main__":
    app.run(debug=True)
