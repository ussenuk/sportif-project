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
        print("5. Top-up your balance")
        print("6. Exit")

        choice = input ("Enter your choice (1-6): ")

        if choice == "1":
            # Registration and subscription combined
            try:
                # Add registration details (ensure complete values)
                member = Member()
                registration_info = member.get_registration_details()
                print("Registration details:", registration_info)  # Verify contents

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
                    # print(f" {index+1}. {subscription.name} (Price: {subscription.price}KES)")
                    print(f" {index+1}. {subscription.name} (Price: {subscription.price} KES)")
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
                     # Deduct 5 KES from balance
                    if member_instance.balance >= 3:
                        member_instance.balance -= 3
                        session.commit()
                        print("3 KES deducted from your balance for this login session. New balance:", member_instance.balance)
                        print("Enjoy Browsing Your Sport News")
                        member_instance.get_all_news_related_to_subscription(session)
                    else:
                        print("Insufficient balance to deduct 3 KES for login. Please top up to continue.")
                        # Call top-up functionality here
                        

                else:
                    print("Invalid username or password. Please try again.")
        
        elif choice == "3":
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            member = session.query(Member).filter_by(username=username).first()
            if member:
                if member.validate_member_credentials(session, username, password):
                    print("Welcome back, {}!".format(member.username))
                    # List subscriptions
                    member.list_subscriptions(session)
                    # Member is logged in, proceed with additional subscription
                    print("\nAvailable subscriptions:")
                    subscriptions = session.query(Subscription).all()
                    if not subscriptions:
                        print("There are currently no subscriptions available.")
                        continue
                    for index, subscription in enumerate(subscriptions):
                        print(f" {index+1}. {subscription.name} (Price: {subscription.price} KES)")

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

                        # # **NEW: Immediately display related news**
                        # member.get_all_news_related_to_subscription(session)
                    except ValueError as e:
                        print(f"Error: {e}")
                        session.rollback()

        elif choice == "4":
            # Cancel subscription
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            member = session.query(Member).filter_by(username=username).first()

            if member:
                if member.validate_member_credentials(session, username, password):
                    print("Welcome back, {}!".format(member.username))

                    # List subscriptions
                    member.list_subscriptions(session)

                    if not member.subscriptions:
                        print("You don't have any subscriptions to cancel.")
                        continue

                    # Prompt user to select subscription to cancel
                    while True:
                        try:
                            subscription_choice = int(input("Enter the number of the subscription you want to cancel: "))
                            if 1 <= subscription_choice <= len(member.subscriptions):
                                break
                            else:
                                print("Invalid choice. Please choose a number between 1 and", len(member.subscriptions))
                        except ValueError:
                            print("Invalid input. Please enter a number.")

                    subscription_to_cancel = member.subscriptions[subscription_choice - 1]

                    # Confirm cancellation with user
                    confirmation = input(f"Are you sure you want to cancel {subscription_to_cancel.name}? (y/n): ")
                    if confirmation.lower() == 'y':
                        try:
                            member.subscriptions.remove(subscription_to_cancel)
                            session.commit()
                            print(f"Subscription {subscription_to_cancel.name} has been cancelled.")
                        except Exception as e:
                            print(f"Error canceling subscription: {e}")
                            session.rollback()

                else:
                    print("Invalid username or password. Please try again.")
            else:
                print("No member found with that username.")
                        
                
        elif choice == "5":
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            member = session.query(Member).filter_by(username=username).first()

            if member:
                if member.validate_member_credentials(session, username, password):
                    print("Welcome back, {}!".format(member.username))

                    while True:
                        try:
                            top_up_amount = float(input("Enter the amount you want to top up (KES): "))
                            if top_up_amount <= 0:
                                raise ValueError("Invalid top-up amount. Please enter a positive number.")
                            break
                        except ValueError:
                            print("Invalid input. Please enter a valid amount.")

                    member.top_up(session, top_up_amount)
                    print("Top-up successful! Your new balance is {} KES.".format(member.balance))
                else:
                    print("Invalid username or password. Please try again.")
            else:
                print("No member found with that username.")
        elif choice == "6":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")