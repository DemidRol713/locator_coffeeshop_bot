from service.coffeeshop_nearby_service import CoffeeShopNearbyService


class CoffeeShopsNearPageController:

    def __init__(self, session):
        self.session = session

    def get_coffeeshop_nearby(self, user_latitude, user_longitude):
        """
        Возвращает данные кофейн рядом с пользователем
        :param user_latitude:
        :param user_longitude:
        :return:
        """
        coffeeshop_service = CoffeeShopNearbyService(session=self.session)

        coffeeshop_list = coffeeshop_service.get_coffeeshop_nearby(user_latitude, user_longitude)
        coffeeshop_list_view = []
        for coffeeshop in coffeeshop_list:
            coffeeshop_view = {
                'text': '{name}  {distance} км'.format(
                    name=coffeeshop.name,
                    distance=coffeeshop.distance
                ),
                'callback_data': 'coffeeshop_{}'.format(coffeeshop.id)
            }

            coffeeshop_list_view.append(coffeeshop_view)

        return coffeeshop_list_view
