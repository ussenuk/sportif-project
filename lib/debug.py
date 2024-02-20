#!/usr/bin/env python3
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Subscription, Member, News

import ipdb;


if __name__ == '__main__':
    
    engine = create_engine('sqlite:///sportif.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    while True:
        print("\nWelcome to Sportif!")
        print("1. Register as a member and subscribe to your sport news")
        print("2. Member proceed to their News")
        print("3. Subscribe to another plan")
        print("4. Cancel subscription")
        print("5. Exit")

        choice = input ("Enter your choice (1-5): ")

        if choice == "1":
            # Registration and subscription combined
            try:
                # Add registration details (ensure complete values)
                member = Member()
                registration_info = member.get_registration_details()
                # print("Registration details:", registration_info)  # Verify contents

                member.add_member(session, **registration_info)
                session.commit()

                # Welcome message with correct name
                welcome_name = registration_info["first_name"]
                print(f"Welcome, {welcome_name}! You're now registered as a member.")

                # Member identification
                member_id = input("Enter your username with your registered account: ")
                # Validate existence of member using query
                member = session.query(Member).filter_by(username=member_id).first()
                if not member:
                    print("No member found with the provided ID. Please double-check and try again.")
                    exit()

                #Display available subscriptions:**
                print("\nNow let's choose a subscription:")
                subscriptions = session.query(Subscription).all()
                if not subscriptions:
                    print("There are currently no subscriptions available.")
                    continue
                
                # Display subscriptions with numeric choices
                for index, subscription in enumerate(subscriptions):
                    print(f" {index+1}. {subscription.name} (Price: {subscription.price}KES)")
                #User choice and validation:**
                while True:
                    try:
                        subscription_choice = int(input("Enter the number of the subscription you want to subscribe to: "))
                        if 1 <= subscription_choice <= len(subscriptions):
                            break
                        else:
                            print("Invalid choice. Please choose a number between 1 and", len(subscriptions))
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                subscription = subscriptions[subscription_choice - 1]
                
                #Subscribe using the method:**
                try:
                    # subscription = session.query(Subscription).filter_by(name=subscription_name).first()
                    member.subscribe_to_subscription(session, subscription.id)
                    session.commit()
                    print(f"Congratulations, {member.first_name}! You are now subscribed to {subscription.name}.")

                    # **NEW: Immediately display related news**
                    member.get_all_news_related_to_subscription(session)
                except ValueError as e:
                    print(f"Error: {e}")
                    session.rollback()
                
                # now access the news
                

            except Exception as e:
                print(f"Registration Error: {e}")
                session.rollback()
        elif choice =="2":
            # Member Login
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            # member = Member()
            member_instance = session.query(Member).filter_by(username=username).first()

            if member_instance:
                # Member found, proceed to their news
                # (Implement news access logic here)
                logged_member = member_instance.validate_member_credentials(session, username, password)
                if logged_member:
                    print(f"Welcome back, {member_instance.username}!\n Your subscription is valid and your balance is {member_instance.balance} KES")
                    # proceed to the news immediately
                    # Access and display news using get_all_news_related_to_subscription
                    member_instance.get_all_news_related_to_subscription(session)


                else:
                    print("Invalid username or password. Please try again.")

                

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")