import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import current_timestamp
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, index=True)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    email = Column(String(120), index=True)
    image = Column(String(250))


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    description = Column(String(250))
    image = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    timestamp = Column(DateTime, default=current_timestamp())
    category = relationship(Category)
    user = relationship(User)


engine = create_engine('sqlite:///itemsCatalog.db')

Base.metadata.create_all(engine)
