from service.coffeeshop_list_service import CoffeeshopListService


class CoffeeShopListPageController:

    def __init__(self):
        pass

    def get_coffeeshop_list(self, page):
        """
        Возвращает список всех кофеен постранично
        :param page: номер страницы
        :return:
        """
        coffeeshop_service = CoffeeshopListService()

        coffeeshop_list, count = coffeeshop_service.get_coffeeshop_list(page)
        coffeeshop_list_view = []
        for coffeeshop in coffeeshop_list:
            coffeeshop_view = {
                'text': f'{coffeeshop.name} на 📍{coffeeshop.address}',
                'callback_data': f'coffeeshop_{coffeeshop.id}'
            }

            coffeeshop_list_view.append(coffeeshop_view)

        count = count // 10 if count % 10 == 0 else count // 10 + 1

        return coffeeshop_list_view, count
