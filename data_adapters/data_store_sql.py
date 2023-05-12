import sqlalchemy
from sqlalchemy import create_engine


class DataStoreSql():

    def __init__(self):

        engine = create_engine("postgresql+psycopg2://demidrol:1q2w3e@localhost/mydb")
        engine.connect()
