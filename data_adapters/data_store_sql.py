from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class DataStoreSql():

    def __init__(self, session: Session, model):

        self.session = session
        self.model = model

    def get_all(self):

        return self.session.query(self.model).all()

    def get_by_id(self, id: int):

        return self.session.query(self.model).get(id)



