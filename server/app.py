#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakery_list=[]
    for baker in Bakery.query.all():
        bakery_dict= {
            "id":baker.id,
            "name" :baker.name,
            "created_at":baker.created_at,
            "updated_at ":baker.updated_at 
            }
        bakery_list.append(bakery_dict)
        response = make_response(
        jsonify(bakery_list),
        200
    )
    response.headers["Content-Type"] = "application/json"


    return response
        
    

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()

    bakery_dict = bakery.to_dict()

    response = make_response(
        jsonify(bakery_dict),
        200
    )
    response.headers["Content-Type"] = "application/json"

    return response
    

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_list = []
    for bake in BakedGood.query.order_by(BakedGood.price.desc()).all():
        bake_dict = {
            "id": bake.id,
            "name": bake.name,
            "price": bake.price,
            "created_at": bake.created_at,
            "updated_at": bake.updated_at
        }
        baked_list.append(bake_dict)

    response = make_response(jsonify(baked_list), 200)
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()

    if most_expensive:
        baked_dict = {
            "id": most_expensive.id,
            "name": most_expensive.name,
            "price": most_expensive.price,
            "created_at": most_expensive.created_at,
            "updated_at": most_expensive.updated_at
        }
        response = make_response(jsonify(baked_dict), 200)
    else:
        response = make_response(jsonify({"error": "No baked goods found"}), 404)

    response.headers["Content-Type"] = "application/json"
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
