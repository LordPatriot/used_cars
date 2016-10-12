# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import jsonify
import Car_pb2
import uuid


# create the Flask application
app = Flask(__name__)


@app.route("/cars", methods=["GET"])
def list_cars():
    return "Cars list will appear here"


@app.route("/car/new", methods=["POST"])
def create_car():
    mark = request.args.get('mark')
    model = request.args.get('model')
    year = int(request.args.get('year'))

    car = Car_pb2.Car()
    car.mark = mark
    car.model = model
    car.year = year
    car.id = uuid.uuid1().hex

    # for now let's throw bytes
    buf = car.SerializeToString()

    return buf


@app.route("/car/<string:id>/price/<string:new_price>", methods=["PUT"])
def update_car_price(id, new_price):
    return "New price is" + new_price


if __name__ == "__main__":
    app.run(debug=True)
