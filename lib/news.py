from sqlalchemy import Column, Integer,Float, String, DateTime, Table, ForeignKey, desc, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from .models import Base

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
