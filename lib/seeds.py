#!/usr/bin/env python3

# Script goes here!
from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Subscription, Member, News

if __name__ == '__main__':
    engine = create_engine('sqlite:///sportif.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Subscription).delete()
    session.query(Member).delete()
    session.query(News).delete()

    fake = Faker()



    for _ in range(5):
        member = Member(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            gender=random.choice(['Male', 'Female']),
            email=fake.email(),
            city=fake.city(),
            country=fake.country(),
            age=random.randint(18, 65),
            username=fake.user_name(),
            password=fake.password(),
            balance=random.uniform(0, 1000)
        )

        # add and commit individually to get IDs back
        session.add(member)
        session.commit()



    subscription_names = {
        'Football': 50,
        'Basketball': 60,
        'Others': 70
    }

    for name, price in subscription_names.items():
        subscription = Subscription(
            name = name,
            price = price,
        )
        # add and commit individually to get IDs back

        session.add(subscription)
        session.commit()


    # for _ in range(5):
    #     news = News(
    #         title=fake.sentence(nb_words=6),
    #         content=fake.text(max_nb_chars=200)
    #     )

    #     # add and commit individually to get IDs back
    #     session.add(news)
    #     session.commit()

    # session.close()