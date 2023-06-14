from model.coffeeshop_manager import CoffeeShopManager


class CoffeeshopListService:

    def __init__(self):

        pass

    def get_coffeeshop_list(self, page):

        coffeeshop_manager = CoffeeShopManager()

        return coffeeshop_manager.get_coffeeshop_list(page)