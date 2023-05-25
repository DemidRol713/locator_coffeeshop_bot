from model.coffeeshop_manager import CoffeeShopManager


class CoffeeshopListService:

    def __init__(self, session):

        self.session = session

    def get_coffeeshop_list(self, page):

        coffeeshop_manager = CoffeeShopManager(self.session)

        return coffeeshop_manager.get_coffeeshop_list(page)