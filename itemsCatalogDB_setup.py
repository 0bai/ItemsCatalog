import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    full_name = Column(String(80), nullable=False)
    username = Column(String(32), index=True)
    email = Column(String(120), nullable=False)
    password_hash = Column(String(64))
    image = Column(String(250))


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    description = Column(String(250))
    image = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    category = relationship(Category)
    user = relationship(User)


engine = create_engine('sqlite:///itemsCatalog.db')

Base.metadata.create_all(engine)
