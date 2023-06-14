from model.coffeeshop_manager import CoffeeShopManager


class CoffeeShopCardService:

    def __init__(self):

        pass

    def get_coffeeshop(self, coffeeshop_id):
        """

        :param coffeeshop_id:
        :return:
        """
        coffeeshop_manager = CoffeeShopManager()

        return coffeeshop_manager.get_coffeeshop_by_id(coffeeshop_id)