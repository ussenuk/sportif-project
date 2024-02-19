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
    price = Column(Integer)

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

