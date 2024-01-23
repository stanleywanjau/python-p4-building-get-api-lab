#!/usr/bin/env python3

from faker import Faker
from random import randint
from datetime import datetime

from app import app
from models import db, Bakery, BakedGood

with app.app_context():
    fake = Faker()

    BakedGood.query.delete()
    Bakery.query.delete()

    # Generate fake data
    NUM_BAKERIES = 5
    NUM_BAKED_GOODS_PER_BAKERY = 10

    for _ in range(NUM_BAKERIES):
        bakery = Bakery(name=fake.company())
        db.session.add(bakery)

        for _ in range(NUM_BAKED_GOODS_PER_BAKERY):
            baked_good = BakedGood(
                name=fake.word(),
                price=randint(1, 10),
                bakery=bakery
            )
            db.session.add(baked_good)

    # Commit the changes to the database
    db.session.commit()

    # Set 'updated_at' for all objects to the current timestamp
    current_time = datetime.utcnow()
    Bakery.query.update({'updated_at': current_time})
    BakedGood.query.update({'updated_at': current_time})

    # Commit the changes to the database
    db.session.commit()

print("Fake data has been successfully generated and added to the database.")
