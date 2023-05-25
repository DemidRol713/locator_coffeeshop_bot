from model.coffeeshop_manager import CoffeeShopManager


class CoffeeShopCardService:

    def __init__(self, session):

        self.session = session

    def get_coffeeshop(self, coffeeshop_id):
        """

        :param coffeeshop_id:
        :return:
        """
        coffeeshop_manager = CoffeeShopManager(self.session)

        return coffeeshop_manager.get_coffeeshop_by_id(coffeeshop_id)