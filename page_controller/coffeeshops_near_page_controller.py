from service.coffeeshop_service import CoffeeShopService

class CoffeeShopsNearPageController:

    def __init__(self):

        pass

    def get_coffeeshops_near(self, user_location):

        coffeeshop_service = CoffeeShopService()