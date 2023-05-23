from model.coffeeshop import CoffeeShop
from data_adapters.data_store_sql import DataStoreSql
# from app import session


class CoffeeShopManager:

    def __init__(self, session):

        self.session = session

    def get_coffeeshop_list(self):
        """
        Возвращает все кофейни
        :return: List(CoffeeShop)
        """
        data_store = DataStoreSql(session=self.session, model=CoffeeShop)

        return data_store.get_data_with_limits(10)

    def get_filtered_coffeeshop_list(self, filter):

        data_store = DataStoreSql(session=self.session, model=CoffeeShop)

        return data_store.get_all()