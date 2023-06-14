from model.coffeeshop_manager import CoffeeShopManager


class SearchCoffeeShop:

    def __init__(self):

        pass

    def get_coffeeshop_by_name(self, name_coffeeshop):

        coffeeshop_manager = CoffeeShopManager()

        return coffeeshop_manager.get_coffeeshop_by_name(name_coffeeshop)

