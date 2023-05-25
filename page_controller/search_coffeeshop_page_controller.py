from service.search_coffeeshop_service import SearchCoffeeShop


class SearchCoffeeShopPageController:

    def __init__(self, session):

        self.session = session

    def get_coffeeshop(self, name_coffeeshop):

        coffeeshop_service = SearchCoffeeShop(self.session)

        coffeeshop_list = coffeeshop_service.get_coffeeshop_by_name(name_coffeeshop)
        coffeeshop_list_view = []
        for coffeeshop in coffeeshop_list:
            coffeeshop_view = {
                'text': f'{coffeeshop.name} на {coffeeshop.address}',
                'callback_data': f'coffeeshop_{coffeeshop.id}'
            }

            coffeeshop_list_view.append(coffeeshop_view)

        return coffeeshop_list_view