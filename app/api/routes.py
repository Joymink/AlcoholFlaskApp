from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Alcohol, alcohol_schema, alcohols_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/Alcohol', methods=['POST'])
@token_required
def create_alcohol(current_user_token):
    brand = request.json['brand']
    category = request.json['category']
    proof = request.json['proof']
    year = request.json['year']
    price = request.json['price']
    user_token = current_user_token.token

    print(f"Here is that User's token: {current_user_token.token}")

    alcohol = Alcohol(brand, category, proof, year, price, user_token= user_token)

    db.session.add(alcohol)
    db.session.commit()

    response = alcohol_schema.dump(alcohol)
    return jsonify(response)

@api.route('/Alcohol', methods = ['GET'])
@token_required
def get_alcohol(current_user_token):
    a_user = current_user_token.token
    alcohols = Alcohol.query.filter_by(user_token = a_user).all()
    response = alcohols_schema.dump(alcohols)
    return jsonify(response)

@api.route('/Alcohol/<id>', methods = ['GET'])
@token_required
def get_single_alcohol(current_user_token, id):
    alcohol = Alcohol.query.get(id)
    response = alcohol_schema.dump(alcohol)
    return jsonify(response)

@api.route('/Alcohol/<id>', methods = ['POST', 'PUT'])
@token_required
def update_alcohol(current_user_token, id):
    alcohol = Alcohol.query.get(id)
    alcohol.brand = request.json['brand']
    alcohol.category = request.json['category']
    alcohol.proof = request.json['proof']
    alcohol.year = request.json['year']
    alcohol.price = request.json['price']
    alcohol.user_token = current_user_token.token

    db.session.commit()
    response = alcohol_schema.dump(alcohol)
    return jsonify(response)

@api.route('/Alcohol/<id>', methods = ['DELETE'])
@token_required
def delete_vehicle(current_user_token, id):
    alcohol = Alcohol.query.get(id)
    db.session.delete(alcohol)
    db.session.commit()
    response = alcohol_schema.dump(alcohol)
    return jsonify(response)