from sqlalchemy import Column, Integer,Float, String, DateTime, Table, ForeignKey, desc, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}

metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)



subscription_member = Table(
    'subscription_members',
    Base.metadata,
    Column('subscription_id', ForeignKey('subscriptions.id'), primary_key=True),
    Column('member_id', ForeignKey('members.id'), primary_key=True),
    extend_existing=True,
)

class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True)
    name = Column(String())
    price = Column(Integer())

    news = relationship('News', backref=backref('subscription'))

    members = relationship('Member', secondary=subscription_member, back_populates='subscriptions')

    def __repr__(self):
        return f'Subscription: {self.name}'
    
class Member(Base):
    __tablename__ = 'members'

    id = Column(Integer, primary_key=True)
    first_name = Column(String())
    last_name = Column(String())
    gender = Column(String())
    email = Column(String())
    city = Column(String())
    country = Column(String())
    age = Column(Integer())
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    balance = Column(Float(), default=0.0)

    news = relationship('News', backref=backref('member'))

    subscriptions = relationship('Subscription', secondary= subscription_member, back_populates='members')

    def get_registration_details(self):
        """
    Prompts the user for registration details and returns them as a dictionary.

    Returns:
        dict: A dictionary containing registration details in the following format:
            {
                'first_name': str,
                'last_name': str,
                'gender': str,
                'email': str,
                'city': str,
                'country': str,
                'age': int,
                'username': str,
                'password': str,
                'balance': int,
            }
    """
        while True:
            first_name = input("Enter your first name:")
            if not first_name:
                print("First name cannot be empty.")
                continue
            last_name = input("Enter your last name:")
            if not last_name:
                print("Last name cannot be empty.")
                continue

            gender = input("Enter your Gender(Male or Female):")
            if not gender:
                print("Last name cannot be empty.")
                continue

            age = input("Enter your age (number only):")
            if not age:
                print("age cannot be empty.")
                continue

            email = input("Enter your email:")
            if not email:
                print("email cannot be empty.")
                continue

            city = input("Enter your city:")
            if not city:
                print("city cannot be empty.")
                continue

            country = input("Enter your country:")
            if not country:
                print("country cannot be empty.")
                continue

            username = input("Enter your username:")
            if not username:
                print("username cannot be empty.")
                continue

            password = input("Enter your password:")
            if not password:
                print("password cannot be empty.")
                continue
            balance = 100

            return {
            'first_name': first_name,
            'last_name': last_name,
            'gender': gender,
            'age': age,
            'email': email,
            'username': username,
            'password': password,
            'city': city,
            'country': country,
            'balance': balance,
        }

            

    def add_member(self, session, first_name, last_name, gender, email, city, country, age, username, password, balance):
        """
        Registers a new member in the database.

        Args:
            session: An SQLAlchemy session object.
            first_name: Member's first name.
            last_name: Member's last name.
            gender: Member's gender.
            email: Member's email address.
            city: Member's city.
            country: Member's country.
            age: Member's age.
            username: Member's username.
            password: Member's password.
        """

        new_member = Member(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            email=email,
            city=city,
            country=country,
            age=age,
            username=username,
            password=password,
            balance = balance,
        )

        session.add(new_member)
        session.commit()

        return new_member
    
    def subscribe_to_subscription(self, session, subscription_id):
        """
        Subscribes this member to a given subscription.

        Args:
            session: An SQLAlchemy session object.
            subscription_id: The ID of the subscription to subscribe to.
        """

        # Check if the member is already subscribed to the subscription
        if subscription_id in [s.id for s in self.subscriptions]:
            raise ValueError("Member is already subscribed to this subscription.")

        
        # Find the subscription object
        subscription = session.query(Subscription).get(subscription_id)
        if not subscription:
            raise ValueError("Subscription with ID {} not found.".format(subscription_id))
        # Check if member has sufficient balance
        if self.balance < subscription.price:
            raise ValueError("Insufficient balance. Please top up before subscribing.")
        
        # Add the subscription to the member's subscriptions
        self.subscriptions.append(subscription)

        # Deduct subscription price from balance
        self.balance -= subscription.price

        #Upadate the member object in the session
        session.add(self)

        # Update the database
        session.commit()

        return subscription
    
    def validate_member_credentials(self,session, username, password):
        """
        Validates member credentials by checking if both username and password match a record in the Member table.

        Args:
            session: A SQLAlchemy session object.
            username: The username entered by the user.
            password: The password entered by the user.

        Returns:
            Member object: If credentials are valid, returns the corresponding Member object.
            None: If credentials are invalid, returns None.
        """

        member = session.query(Member).filter_by(username=username, password=password).first()
        if member:
            # Check if password matches
            if member.password == password:
                return member
            else:
                print("Invalid password. Please try again.")
        else:
            print("No member found with that username.")
            
        return None
    
    def get_all_news_related_to_subscription(self, session):
        """
        Retrieves and displays all news related to the member's subscribed category.

        Args:
            session: An SQLAlchemy session object.

        Returns:
            None: Prints news titles, categories, and content to the console.
        """

        # Get subscribed categories
        subscribed_categories = set([s.name for s in self.subscriptions])

        # Filter news based on subscribed categories
        filtered_news = session.query(News).filter(News.category.in_(subscribed_categories)).all()

        # Check if any news found
        if not filtered_news:
            print("You don't have access to any news yet in your subscribed categories. Subscribe to some relevant subscriptions!")
            return

        # Initialize variables
        current_index = 0
        news_length = len(filtered_news)

        while True:
            # Display current news details
            news = filtered_news[current_index]
            print(f"Title: {news.title}")
            print(f"Category: {news.category}")
            print(f"Content: {news.content}\n")

            # User choice
            choice = input("Enter '1' to see the next news, or '2' to quit: ")

            # Handle user input
            if choice.lower() == "1":
                current_index += 1
                if current_index >= news_length:
                    print("No more news to display.")
                    break
            elif choice.lower() == "2":
                break
            else:
                print("Invalid input. Please enter '1' or '2'.")
    
        
    
    
    def __repr__(self):
        return f'Member: {self.name}'
    
class News(Base):
    __tablename__ = 'news'

    id = Column(Integer(), primary_key=True)
    title = Column(String(80))
    content= Column(String(200))
    category =Column(String())


    subscription_id = Column(Integer(), ForeignKey('subscriptions.id'))

    member_id = Column(Integer(), ForeignKey('members.id'))

    def __repr__(self):
        return f'News(id={self.id},' + \
            f'title={self.title}, ' + \
            f'subscription_id={self.subscription_id}, ' + \
            f'member_id={self.member_id})'

