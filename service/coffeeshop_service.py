from math import radians, cos, sin, sqrt, asin
import geopy.distance

from database.model import CoffeeShop


class CoffeeShopService:

    def __init__(self):
        pass

    def calculates_the_distance(self, user_coordinate, coffeeshop_coordinate):

        return geopy.distance.geodesic(user_coordinate, coffeeshop_coordinate).km
