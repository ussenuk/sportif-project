# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from models import Member, Subscription

# # Additional code for database initialization and session creation
# engine = create_engine('sqlite:///sportif.db')
# Session = sessionmaker(bind=engine)
# session = Session()

# def register(first_name, last_name, gender, email, city, country, age, username, password,balance):
#     member = session.query(Member).first()





    # # Query all subscriptions
    # subscriptions = session.query(Subscription).all()

    # # For each subscription, print its name and the first_name of its members
    # for subscription in subscriptions:
    #     print(f'Subscription: {subscription.name}')
    #     print('Members:')
    #     for member in subscription.members:
    #         print(f'- {member.first_name}')


    # # Query all members
    # members = session.query(Member).all()

    # # For each dev, print its name and the names of its companies
    # for member in members:
    #     print(f'Member: {member.first_name}')
    #     print('Subscription:')
    #     for subscription in member.subscriptions:
    #         print(f'- {subscription.name}')


