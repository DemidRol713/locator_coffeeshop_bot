from math import radians, cos, sin, sqrt, asin
import geopy.distance

from model.coffeeshop_manager import CoffeeShopManager


class CoffeeShopService:

    def __init__(self, session):

        self.session = session

    def get_coffeeshop_nearby(self, user_coordinate):
        """
        Возвращает кофейни в радиусе 2 км
        :param user_coordinate: координаты пользователя
        :return: List(CoffeeShop)
        """
        coffeeshop_manager = CoffeeShopManager(self.session)

        coffeeshop_list = coffeeshop_manager.get_coffeeshop_list()
        coffeeshop_nearby_list = []
        for coffeeshop in coffeeshop_list:
            distance = geopy.distance.geodesic(user_coordinate, {coffeeshop.latitude, coffeeshop.longitude}).km
            # if distance <= 2:
            coffeeshop.distance = distance
            coffeeshop_nearby_list.append(coffeeshop)

        return coffeeshop_nearby_list
