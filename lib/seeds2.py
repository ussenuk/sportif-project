# #!/usr/bin/env python3

# # Script goes here!
# from faker import Faker
# import random

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# from models import Subscription, Member, News, SubscriptionDuration

# if __name__ == '__main__':
#     engine = create_engine('sqlite:///sportif.db')
#     Session = sessionmaker(bind=engine)
#     session = Session()

#     # Clear existing data
#     session.query(Subscription).delete()
#     session.query(Member).delete()
#     session.query(News).delete()
#     session.query(SubscriptionDuration).delete()

#     fake = Faker()

#     # Create members
#     members = []
#     for _ in range(5):
#         member = Member(
#             first_name=fake.first_name(),
#             last_name=fake.last_name(),
#             gender=random.choice(['Male', 'Female']),
#             email=fake.email(),
#             city=fake.city(),
#             country=fake.country(),
#             age=random.randint(18, 65),
#             username=fake.user_name(),
#             password=fake.password(),
#             balance=random.uniform(0, 1000)
#         )

#         # Add and commit individually to get IDs back
#         session.add(member)
#         session.commit()

#         members.append(member)

#     # Create subscription durations
#     subscription_durations = []
#     for duration, price in zip([30, 60], [25, 50]):
#         subscription_duration = SubscriptionDuration(
#             duration=duration,
#             price=price
#         )
#         session.add(subscription_duration)
#         session.commit()

#         subscription_durations.append(subscription_duration)

#     # Create subscriptions
#     subscriptions = []
#     subscription_names = ['Football', 'Basketball', 'Others']
#     for name in subscription_names:
#         duration = random.choice(subscription_durations)
#         subscription = Subscription(
#             name=name,
#             duration=duration,  # link to duration object instead of setting duration directly
#             # end_date will be calculated at activation automatically
#         )
#         session.add(subscription)
#         session.commit()

#         subscriptions.append(subscription)

#     # Create news
#     news = []
#     for member in members:
#         for subscription in subscriptions:
#             for i in range(random.randint(1, 5)):
#                 new = News(
#                     title=fake.sentence(nb_words=6),
#                     content=fake.text(max_nb_chars=200),
#                     category=random.choice(subscription_names),
#                     subscription_id=subscription.id,
#                     member_id=member.id
#                 )
#                 news.append(new)

#     # Save news to the database
#     session.bulk_save_objects(news)
#     session.commit()

#     session.close()