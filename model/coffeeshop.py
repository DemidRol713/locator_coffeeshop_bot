from sqlalchemy import Integer, String, Column, Text, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CoffeeShop(Base):
    
    __tablename__ = 'coffeeshop_coffeeshop'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    address = Column(String(500), nullable=False)
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