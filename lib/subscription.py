from sqlalchemy import Column, Integer,Float, String, DateTime, Table, ForeignKey, desc, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from .models import Base, metadata



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