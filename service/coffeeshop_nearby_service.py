from math import radians, cos, sin, sqrt, asin
import geopy.distance

from model.coffeeshop_manager import CoffeeShopManager


class CoffeeShopNearbyService:

    def __init__(self, session):

        self.session = session

    def get_coffeeshop_nearby(self, user_latitude, user_longitude):
        """
        Возвращает кофейни в радиусе 2 км
        :param user_latitude: широта пользователя
        :param user_longitude: долгота пользователя
        :return:
        """
        coffeeshop_manager = CoffeeShopManager(self.session)

        coffeeshop_list = coffeeshop_manager.get_coffeeshop_list()
        coffeeshop_nearby_list = []
        for coffeeshop in coffeeshop_list:
            distance = geopy.distance.geodesic((user_latitude, user_longitude), (coffeeshop.latitude, coffeeshop.longitude)).km
            if distance <= 2:
                coffeeshop.distance = round(distance, 2)
                coffeeshop_nearby_list.append(coffeeshop)

        return sorted(coffeeshop_nearby_list, key=lambda item: item.distance)
