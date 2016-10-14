# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import jsonify
from flask import url_for, redirect
import Car_pb2
import uuid
import redis


# create the Flask application
app = Flask(__name__)


# add redis as a storage
r = redis.Redis(host='127.0.0.1', port=6379)


@app.route("/cars", methods=["GET"])
def list_cars():
    # really bad idea in production, but ok for now
    return jsonify(r.keys(pattern='*'))


@app.route("/car/new", methods=["POST"])
def create_car():
    mark = request.args.get('mark')
    model = request.args.get('model')
    year = int(request.args.get('year'))

    car = Car_pb2.Car()
    car.mark = mark
    car.model = model
    car.year = year
    car_id = uuid.uuid1().hex
    car.id = car_id

    buf = car.SerializeToString()
    r.set(car_id, buf)
    return redirect(url_for("get_car", car_id=car_id))


@app.route("/car/<string:car_id>", methods=["GET"])
def get_car(car_id):
    car = fetch_car(car_id)
    # let's print something
    return jsonify([car.id, car.mark, car.model, car.year])


def fetch_car(car_id):
    car = Car_pb2.Car()
    buf = r.get(car_id)
    if buf is None:
        return None

    car.ParseFromString(buf)
    return car


if __name__ == "__main__":
    app.run(debug=True)
