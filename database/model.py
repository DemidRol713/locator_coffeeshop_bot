import sqlalchemy
from sqlalchemy import Table, Index, Integer, String, Column, Text, \
    DateTime, Boolean, PrimaryKeyConstraint, \
    UniqueConstraint, ForeignKeyConstraint, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class CoffeeShop(Base):
    __tablename__ = 'coffeeshop_coffeeshop'
    id = Column(Integer)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    opening_hours = Column(Text, nullable=False)
    social_networks = Column(String(200), nullable=False)
    website = Column(String(200), nullable=False)
    telephone = Column(String(200), nullable=False)
    email = Column(String(254), nullable=False)
    images = Column(String(100))
    tags = Column(String(30))
