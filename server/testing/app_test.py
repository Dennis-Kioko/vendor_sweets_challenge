import json
from os import environ
from flask import request
from faker import Faker
from app import app
from models import db, Sweet, Vendor, VendorSweet
from random import randint


class TestApp:
    '''Flask application in app.py'''

    def test_gets_vendors(self):
        '''retrieves vendors with GET requests to /vendors.'''

        with app.app_context():
            fake = Faker()
            vendor1 = Vendor(name=fake.name())
            vendor2 = Vendor(name=fake.name())
            db.session.add_all([vendor1, vendor2])
            db.session.commit()

            vendors = Vendor.query.all()

            response = app.test_client().get('/vendors')
            assert response.status_code == 200
            assert response.content_type == 'application/json'
            response = response.json
            assert [vendor['id'] for vendor in response] == [
                vendor.id for vendor in vendors]
            assert [vendor['name'] for vendor in response] == [
                vendor.name for vendor in vendors]
            for vendor in response:
                assert 'vendor_sweets' not in vendor

    def test_gets_vendor_by_id(self):
        '''retrieves one vendor using its ID with GET request to /vendors/<int:id>.'''

        with app.app_context():
            fake = Faker()
            vendor = Vendor(name=fake.name())
            db.session.add(vendor)
            db.session.commit()

            response = app.test_client().get(
                f'/vendors/{vendor.id}')
            assert response.status_code == 200
            assert response.content_type == 'application/json'
            response = response.json
            assert response['id'] == vendor.id
            assert response['name'] == vendor.name
            assert 'vendor_sweets' in response

    def test_returns_404_if_no_vendor_to_get(self):
        '''returns an error message and 404 status code with GET request to /vendors/<int:id> by a non-existent ID.'''

        with app.app_context():
            response = app.test_client().get('/vendors/0')
            assert response.status_code == 404
            assert response.content_type == 'application/json'
            assert response.json.get('error') == "Vendor not found"
            assert response.status_code == 404

    def test_gets_sweets(self):
        '''retrieves sweets with GET requests to /sweets.'''

        with app.app_context():
            fake = Faker()
            sweet1 = Sweet(name=fake.name())
            sweet2 = Sweet(name=fake.name())
            db.session.add_all([sweet1, sweet2])
            db.session.commit()

            sweets = Sweet.query.all()

            response = app.test_client().get('/sweets')
            assert response.status_code == 200
            assert response.content_type == 'application/json'
            response = response.json
            assert [sweet['id'] for sweet in response] == [
                sweet.id for sweet in sweets]
            assert [sweet['name'] for sweet in response] == [
                sweet.name for sweet in sweets]
            for sweet in response:
                assert 'vendor_sweets' not in sweet

    def test_gets_sweet_by_id(self):
        '''retrieves one sweet using its ID with GET request to /sweets/<int:id>.'''

        with app.app_context():
            fake = Faker()
            sweet = Sweet(name=fake.name())
            db.session.add(sweet)
            db.session.commit()

            response = app.test_client().get(
                f'/sweets/{sweet.id}')
            assert response.status_code == 200
            assert response.content_type == 'application/json'
            response = response.json
            assert response['id'] == sweet.id
            assert response['name'] == sweet.name
            assert 'vendor_sweets' not in response

    def test_returns_404_if_no_sweet_to_get(self):
        '''returns an error message and 404 status code with GET request to /sweets/<int:id> by a non-existent ID.'''

        with app.app_context():
            response = app.test_client().get('/sweets/0')
            assert response.status_code == 404
            assert response.content_type == 'application/json'
            assert response.json.get('error') == "Sweet not found"
            assert response.status_code == 404

    def test_creates_sweet_vendor(self):
        '''creates one VendorSweet using, price, sweet_id, and a vendor_id with a POST request to /vendor_sweets.'''

        with app.app_context():
            fake = Faker()
            sweet = Sweet(name=fake.name())
            vendor = Vendor(name=fake.name())

            db.session.add(sweet)
            db.session.add(vendor)
            db.session.commit()

            # delete if existing in case price differs
            vendor_sweet = VendorSweet.query.filter_by(
                vendor_id=vendor.id, sweet_id=sweet.id).one_or_none()
            if vendor_sweet:
                db.session.delete(vendor_sweet)
                db.session.commit()

            price = randint(1, 20)
            response = app.test_client().post(
                '/vendor_sweets',
                json={
                    "price": price,
                    "vendor_id": vendor.id,
                    "sweet_id": sweet.id,
                }
            )

            assert response.status_code == 201
            assert response.content_type == 'application/json'
            response = response.json
            assert response['price'] == price
            assert response['vendor_id'] == vendor.id
            assert response['sweet_id'] == sweet.id
            assert response['id']
            assert response['sweet']['name'] == sweet.name
            assert response['sweet']['id'] == sweet.id
            assert response['vendor']['id'] == vendor.id
            assert response['vendor']['name'] == vendor.name

            query_result = VendorSweet.query.filter(
                VendorSweet.vendor_id == vendor.id, VendorSweet.sweet_id == sweet.id).first()
            assert query_result.price == price

    def test_400_for_validation_error(self):
        '''returns a 400 status code and error message if a POST request to /vendor_sweets fails.'''
        with app.app_context():
            fake = Faker()
            sweet = Sweet(name=fake.name())
            vendor = Vendor(name=fake.name())

            db.session.add(sweet)
            db.session.add(vendor)
            db.session.commit()

            response = app.test_client().post(
                '/vendor_sweets',
                json={
                    "price": -1,
                    "vendor_id": vendor.id,
                    "sweet_id": sweet.id,
                }
            )
            assert response.status_code == 400
            assert response.json['errors'] == ["validation errors"]


    def test_deletes_vendor_sweet_by_id(self):
        '''deletes one VendorSweet with DELETE request to /vendor_sweets/<int:id>.'''

        with app.app_context():
            fake = Faker()
            sweet = Sweet(name=fake.name())
            vendor = Vendor(name=fake.name())

            db.session.add_all([sweet, vendor])
            db.session.commit()

            vendor_sweet = VendorSweet(
                vendor_id=vendor.id, sweet_id=sweet.id, price=10)
            db.session.add(vendor_sweet)
            db.session.commit()

            response = app.test_client().delete(
                f'/vendor_sweets/{vendor_sweet.id}')

            assert response.status_code == 204

            result = VendorSweet.query.filter(
                VendorSweet.vendor_id == vendor.id, VendorSweet.sweet_id == sweet.id).one_or_none()
            assert result is None

    def test_returns_404_if_no_vendor_sweet_to_delete(self):
        '''returns an error message and 404 status code with DELETE request to /vendor_sweets/<int:id> by a non-existent ID.'''

        with app.app_context():
            response = app.test_client().delete('/vendor_sweets/0')
            assert response.status_code == 404
            assert response.json.get('error') == "VendorSweet not found"