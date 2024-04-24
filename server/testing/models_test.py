import pytest
from app import app
from models import db, Sweet, Vendor, VendorSweet
from faker import Faker


class TestVendorSweet:
    '''Class VendorSweet in models.py'''

    def test_price_0_or_greater(self):
        '''requires price >= 0.'''

        with app.app_context():

            sweet = Sweet(name=Faker().name(), )
            vendor = Vendor(name=Faker().name())
            db.session.add_all([sweet, vendor])
            db.session.commit()

            vendor_sweet = VendorSweet(
                vendor_id=vendor.id, sweet_id=sweet.id, price=0)
            db.session.add(vendor_sweet)
            db.session.commit()

    def test_price_too_low(self):
        '''requires non negative price .'''

        with app.app_context():

            with pytest.raises(ValueError):
                sweet = Sweet(name=Faker().name(), )
                vendor = Vendor(name=Faker().name())
                db.session.add_all([sweet, vendor])
                db.session.commit()

                vendor_sweet = VendorSweet(
                    vendor_id=vendor.id, sweet_id=sweet.id, price=-1)
                db.session.add(vendor_sweet)
                db.session.commit()

    def test_price_none(self):
        '''requires non negative price .'''

        with app.app_context():

            with pytest.raises(ValueError):
                sweet = Sweet(name=Faker().name(), )
                vendor = Vendor(name=Faker().name())
                db.session.add_all([sweet, vendor])
                db.session.commit()

                vendor_sweet = VendorSweet(
                    vendor_id=vendor.id, sweet_id=sweet.id, price=None)
                db.session.add(vendor_sweet)
                db.session.commit()
