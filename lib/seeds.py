#!/usr/bin/env python3

# Script goes here!
from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Subscription, Member, News, subscription_member

if __name__ == '__main__':
    engine = create_engine('sqlite:///sportif.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Subscription).delete()
    session.query(Member).delete()
    session.query(News).delete()
    session.query(subscription_member).delete()

    fake = Faker()


    members = []
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

        members.append(member)



    subscriptions = []
    subscription_names = {
        'Football': 5,
        'Basketball': 6,
        'Others': 7
    }

    for name, price in subscription_names.items():
        subscription = Subscription(
            name = name,
            price = price,
        )
        # add and commit individually to get IDs back

        session.add(subscription)
        session.commit()

        subscriptions.append(subscription)

    news = []
    for member in members:
        for subscription in subscriptions:
            #For each subscription, it picks a random number of members (between 1 and 5) to subscribe to news
            for i in range(random.randint(1,5)):
                member = random.choice(members)

                # Add the news 
                new = News(
                    title=fake.sentence(nb_words=6),
                    content=fake.text(max_nb_chars=200),
                    category=random.choice(list(subscription_names.keys())),
                    subscription_id=subscription.id,
                    member_id=member.id
                )

                news.append(new)
        # save all news to the database
                
    session.bulk_save_objects(news)
    session.commit()

    session.close()
