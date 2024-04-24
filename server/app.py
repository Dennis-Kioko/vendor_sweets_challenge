#!/usr/bin/env python3

from models import db, Sweet, Vendor, VendorSweet
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from sqlalchemy.orm.exc import NoResultFound
import os
from dotenv import load_dotenv
load_dotenv()

# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DATABASE = os.environ.get(
#     "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")
# 

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] =os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Code challenge</h1>'

@app.route('/vendors')
def get_vendors():
    vendors = Vendor.query.all()
    vendor_data = [{
        "id": vendor.id,
        "name": vendor.name
    } for vendor in vendors]
    return jsonify(vendor_data), 200

@app.route('/vendors/<int:id>', methods=['GET'])
def vendor_by_id(id):
    vendor = Vendor.query.filter_by(id=id).first()

    if request.method == 'GET':
        if vendor:
            vendor_data = {
                'id': vendor.id,
                'name': vendor.name,
                'vendor_sweets': [{
                    'id': vendor_sweet.id,
                    'price': vendor_sweet.price,
                    'sweet': {
                        'id': vendor_sweet.sweet.id,
                        'name': vendor_sweet.sweet.name
                    },
                    'sweet_id': vendor_sweet.sweet_id,
                    'vendor_id': vendor_sweet.vendor_id
                } for vendor_sweet in vendor.vendor_sweets]
            }
            return jsonify(vendor_data), 200
        else:
            return make_response(
                {"error": "Vendor not found"},
                404
                )

@app.route('/sweets')
def get_sweets():
    sweets = Sweet.query.all()
    sweet_data = [{
        "id": sweet.id,
        "name": sweet.name
    } for sweet in sweets]
    return jsonify(sweet_data), 200

@app.route('/sweets/<int:id>', methods=['GET'])
def sweet_by_id(id):
    sweet = Sweet.query.filter_by(id=id).first()

    if request.method == 'GET':
        if sweet:
            sweet_data = {
                "id": sweet.id,
                "name": sweet.name
            }
            return jsonify(sweet_data), 200
        else:
            return make_response(
                {"error": "Sweet not found"},
                404
                )

@app.route('/vendor_sweets', methods=['GET', 'POST'])
def get_and_post_vendor_sweets():
    if request.method == 'GET':
        vendor_sweets = VendorSweet.query.all()
        vendor_sweet_data = [{
            "id": vendor_sweet.id,
            "price": vendor_sweet.price,
            "sweet_id": vendor_sweet.sweet_id,
            "vendor_id": vendor_sweet.vendor_id
        } for vendor_sweet in vendor_sweets]
        return jsonify(vendor_sweet_data), 200
    
    elif request.method == 'POST':
        data = request.get_json()
        if all(key in data for key in ("price", "vendor_id", "sweet_id")):
                try:
                    price = int(data["price"])
                    if price < 0:
                        return jsonify({"errors": ["validation errors"]}), 400  
                except ValueError:
                    return jsonify({"errors": ["Invalid price format"]}), 400
        
                vendor_id = data["vendor_id"]
                sweet_id = data["sweet_id"]
                vendor = Vendor.query.filter_by(id=vendor_id).one_or_none()
                sweet = Sweet.query.filter_by(id=sweet_id).one_or_none()
                
                if vendor and sweet:
                        new_vendor_sweets = VendorSweet(
                            price=price, vendor_id=vendor_id, sweet_id=sweet_id
                        )
                        db.session.add(new_vendor_sweets)
                        db.session.commit()
                
                        response_data = {
                            "id": new_vendor_sweets.id,
                            "price": new_vendor_sweets.price,
                            "sweet": {
                                "id": sweet.id,
                                "name": sweet.name
                            },
                            "sweet_id": sweet_id,
                            "vendor": {
                                "id": vendor.id,
                                "name": vendor.name
                            },
                            "vendor_id": vendor_id
                        }
                        return make_response(response_data, 201)
                else:
                        error_message = "Vendor not found" if not vendor else "Sweet not found"
                        return jsonify({"errors": [error_message]}), 400 
        else:
            return jsonify({"errors": ["validation errors"]}), 400

@app.route('/vendor_sweets/<int:id>', methods=['DELETE'])
def vendor_sweet_by_id(id):
    try:
        vendor_sweet = VendorSweet.query.filter_by(id=id).one()
        db.session.delete(vendor_sweet)
        db.session.commit()
        return jsonify({}), 204  # Returning an empty response with status code 204 on successful deletion
    except NoResultFound:
        return jsonify({"error": "VendorSweet not found"}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)