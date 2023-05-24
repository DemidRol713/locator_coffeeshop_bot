from model.coffeeshop import CoffeeShop
from data_adapters.data_store_sql import DataStoreSql
# from app import session


class CoffeeShopManager:

    def __init__(self, session):

        self.session = session

    def get_coffeeshop_list(self, page):
        """
        Возвращает все кофейни
        :return: List(CoffeeShop)
        """
        data_store = DataStoreSql(session=self.session, model=CoffeeShop)

        return data_store.get_data_with_pagination(page, 10)

    def get_filtered_coffeeshop_list(self, filter):
        """
        Возвращает отфильтрованные кофейни
        :param filter:
        :return:
        """
        data_store = DataStoreSql(session=self.session, model=CoffeeShop)

        return data_store.get_filtered_data(filter)

    def get_coffeeshop_by_id(self, coffeeshop_id):
        """

        :param coffeeshop_id:
        :return:
        """
        data_store = DataStoreSql(session=self.session, model=CoffeeShop)

        return data_store.get_by_id(coffeeshop_id)