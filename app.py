# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import jsonify
import Car_pb2
import uuid
import redis


# create the Flask application
app = Flask(__name__)

# add redis as a storage
r = redis.Redis(host='127.0.0.1', port=6379)

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
    id = uuid.uuid1().hex
    car.id = id

    buf = car.SerializeToString()
    r.set(id, buf)
    return id


@app.route("/car/<string:id>", methods=["GET"])
def get_car(id):
    car = Car_pb2.Car()
    buf = r.get(id)
    car.ParseFromString(buf)
    # let's print something
    return jsonify([car.id, car.mark, car.model, car.year])


@app.route("/car/<string:id>/price/<string:new_price>", methods=["PUT"])
def update_car_price(id, new_price):
    return "New price is" + new_price


if __name__ == "__main__":
    app.run(debug=True)
