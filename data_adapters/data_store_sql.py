from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from paginate_sqlalchemy import SqlalchemyOrmPage

import config


class DataStoreSql():

    def __init__(self, model):

        engine = create_engine(config.DATA_BASE)
        self.session = Session(bind=engine)
        self.model = model

    def get_all(self):
        """
        Возвращает все данные из таблицы
        :return:
        """
        return self.session.query(self.model).all()

    def get_by_id(self, id: int):
        """
        Возвращает данные объекта по ID
        :param id: ID объекта
        :return:
        """
        return self.session.query(self.model).get(id)

    def get_data_with_limits(self, limit: int):
        """
        Возвращает ограниченное количество данных
        :param limit:
        :return:
        """
        return self.session.query(self.model).limit(limit)

    def get_filtered_data(self, filter: Any):
        """
        Возвращает список отфильтрованных объектов
        :param filter:
        :return:
        """
        return self.session.query(self.model).filter(filter)

    def get_data_with_pagination(self, page: int, amount_data: int):
        """
        Возвращает список объектов частями, постранично
        :param page:
        :param amount_data:
        :return:
        """
        data = SqlalchemyOrmPage(self.session.query(self.model), page, amount_data)
        count = len(self.session.query(self.model).all())

        return data, count

    # def get_data_by_string(self, data: str):
    #     """
    #
    #     :param data:
    #     :return:
    #     """
    #     return self.session.query(self.model).filter(self.model.name.ilike(f'{data}%'))



