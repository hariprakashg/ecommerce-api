from flask import Blueprint, request, jsonify
from . import mongo
from flask_jwt_extended import jwt_required
from bson.objectid import ObjectId

api_bp = Blueprint('api', __name__)

@api_bp.route('/products', methods=['GET'])
def get_products():
    # Optimization: Use projection to only fetch name and price
    products = mongo.db.products.find({}, {"name": 1, "price": 1, "stock": 1})
    output = []
    for p in products:
        output.append({"id": str(p['_id']), "name": p['name'], "price": p['price']})
    return jsonify(output), 200

@api_bp.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    data = request.get_json()
    product_id = mongo.db.products.insert_one({
        "name": data['name'],
        "price": data['price'],
        "stock": data['stock']
    }).inserted_id
    return jsonify({"id": str(product_id)}), 201