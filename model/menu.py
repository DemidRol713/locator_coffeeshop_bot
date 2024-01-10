import sqlalchemy
from sqlalchemy import Table, Index, Integer, String, Column, Text, \
    DateTime, Boolean, PrimaryKeyConstraint, \
    UniqueConstraint, ForeignKeyConstraint, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Menu(Base):

    __tablename__ = 'menu_menu'
    id = Column(Integer, primary_key=True)
    id_coffeeshop = Column()