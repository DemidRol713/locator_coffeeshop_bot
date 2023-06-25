import os

from service.coffeeshop_card_service import CoffeeShopCardService


class CoffeeShopPageController:

    def __init__(self):
        pass

    def get_coffeeshop(self, coffeeshop_id: int):
        """

        :param coffeeshop_id:
        :return:
        """

        coffeeshop_card_service = CoffeeShopCardService()
        coffeeshop = coffeeshop_card_service.get_coffeeshop(coffeeshop_id)
        coffeeshop_view = {
            'text': 'Кофейня <b>{name}</b>\n\n{description}\n\n📍Адрес: {address}\n\nСоц.сети и сайты:\n'.format(
                description=coffeeshop.description,
                address=coffeeshop.address,
                name=coffeeshop.name
            ),
            'latitude': coffeeshop.latitude,
            'longitude': coffeeshop.longitude
            # 'images': coffeeshop.images if coffeeshop.images is not None else []
        }
        for website in coffeeshop.website:
            coffeeshop_view['text'] += website + '\n'

        return coffeeshop_view