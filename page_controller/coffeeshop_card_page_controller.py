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
            'text': 'Кофейня "{name}"\n\n{description}\n\nАдрес:\n{address}\n\nСоц.сети и сайты:\n'.format(
                description=coffeeshop.description,
                address=coffeeshop.address,
                name=coffeeshop.name
            ),
            'images': coffeeshop.images
        }

        for website in coffeeshop.website:
            coffeeshop_view['text'] += website + '\n'