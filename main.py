import os.path
import time

import telebot
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from telebot import types
import logging

import config
from model.coffeeshop import CoffeeShop
from page_controller.coffeeshop_card_page_controller import CoffeeShopPageController
from page_controller.coffeeshop_list_page_controller import CoffeeShopListPageController
from page_controller.coffeeshop_nearby_page_controller import CoffeeShopsNearPageController
from page_controller.search_coffeeshop_page_controller import SearchCoffeeShopPageController

bot = telebot.TeleBot(config.TG_TOKEN)
engine = create_engine(config.DATA_BASE)
session = Session(bind=engine)

logger = telebot.logger
# telebot.logger.basicConfig(filename='filename.log', level=logging.DEBUG,
#                     format=' %(asctime)s - %(levelname)s - %(message)s')
telebot.logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    import app


def get_menu_btn(markup):
    """
    Возвращает список кнопок меню
    :return:
    """
    btn_list = [types.KeyboardButton(btn) for btn in config.MENU]
    for btn in btn_list:
        markup.add(btn)

    return markup


@bot.message_handler(commands=['start'])
def start(message):
    """
    Стартовое сообщение при запуске бота
    :param message:
    :return:
    """

    markup = types.ReplyKeyboardMarkup()
    markup = get_menu_btn(markup)

    bot.send_message(message.from_user.id, "👋 Привет! Я бот-помощник в поиске кофейн поблизости!", reply_markup=markup)


@bot.message_handler(commands=['menu'])
def menu(message):
    """
    Главное меню бота
    :param message:
    :return:
    """
    markup = types.InlineKeyboardMarkup()
    btn_description = types.InlineKeyboardButton(text='Описание бота', callback_data='description')
    btn_coffee_shop_nearby = types.InlineKeyboardButton(text='Кофейни рядом', callback_data='coffee_shop_nearby')
    markup.add(btn_description)
    markup.add(btn_coffee_shop_nearby)

    bot.send_message(message.from_user.id, "Что нужно?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'description')
def description_option_bot(call):
    """
    Описание функций бота
    :param call:
    :return:
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    bot.send_message(call.from_user.id, "Должно быть описание, но пока нет!", reply_markup=markup)


@bot.message_handler(commands=['list_all_coffeeshop'])
def list_coffeeshop(message, page=1):
    """
    Список всех кофеен в базе данных
    :param message:
    :return:
    """
    markup = types.InlineKeyboardMarkup()
    page_controller = CoffeeShopListPageController(session)

    coffeeshop_list, count = page_controller.get_coffeeshop_list(page)
    for coffeeshop in coffeeshop_list:
        markup.add(types.InlineKeyboardButton(text=coffeeshop['text'], callback_data=coffeeshop['callback_data']))

    markup = pagination(markup, page, count)

    bot.send_message(message.from_user.id, "Кофейни Спб: ", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: 'coffeeshop' in call.data)
def coffeeshop_card(call):
    """
    Карточка с данными кофейни
    :param call:
    :return:
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    page_controller = CoffeeShopPageController(session)

    coffeeshop_id = int(call.data.split('_')[-1])

    coffeeshop = page_controller.get_coffeeshop(coffeeshop_id)

    for image_name in coffeeshop['images']:
        image = open(os.path.abspath(config.DATA_FOLDER + image_name), 'rb')
        bot.send_photo(call.from_user.id, image)

    bot.send_message(call.from_user.id, coffeeshop['text'], reply_markup=markup)
    bot.send_location(call.from_user.id, coffeeshop.latitude, coffeeshop.longitude)


@bot.callback_query_handler(func=lambda call: 'coffee_shop_nearby' in call.data)
def user_location(call):
    """
    Просит у пользователя его местоположение
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    geolocation = types.KeyboardButton('Отправить свое местоположения', request_location=True)
    markup.add(geolocation)
    bot.send_message(call.from_user.id, 'Отправьте ваше местоположение, чтобы мы смогли найти кофейни по близости',
                     reply_markup=markup)


@bot.message_handler(content_types=['location'])
def coffeeshop_nearby(message: types.Message):
    """
    Возвращает список кофейн поблизости
    """
    page_controller = CoffeeShopsNearPageController(session)
    markup = types.InlineKeyboardMarkup()

    bot.send_message(message.from_user.id, 'Идет поиск кофеен по близости', reply_markup=get_menu_btn(types.ReplyKeyboardMarkup()))
    tic = time.perf_counter()
    data = page_controller.get_coffeeshop_nearby(message.location.latitude, message.location.longitude)
    # data = page_controller.get_coffeeshop_nearby(60.016208, 30.372300)
    for item in data:
        markup.add(types.InlineKeyboardButton(text=item['text'], callback_data=item['callback_data']))

    toc = time.perf_counter()
    bot.send_message(message.from_user.id, 'В радиусе 2 км:', reply_markup=markup)
    print(f"Вычисление заняло {toc - tic:0.4f} секунд")
    print(len(data))


def pagination(markup, page, amount_data):
    """
    Добавляет пагинацию
    :param markup:
    :param page:
    :param amount_data:
    :return:
    """
    left = page - 1 if page != 1 else amount_data
    right = page + 1 if page != amount_data else 1

    btn_previous = types.InlineKeyboardButton(text='<-', callback_data=f'page {left}')
    btn_page = types.InlineKeyboardButton(text=f'{page}/{amount_data}', callback_data='_')
    btn_next = types.InlineKeyboardButton(text='->', callback_data=f'page {right}')

    markup.add(btn_previous, btn_page, btn_next)

    return markup


@bot.callback_query_handler(func=lambda call: 'page' in call.data)
def callback_page(call):
    """
    Перелистывает страницу
    :param call:
    :return:
    """
    page = call.data.split()[-1]
    if page.isdigit():
        list_coffeeshop(call, int(page))


@bot.message_handler(commands=['search_coffeeshop'])
def search_coffeeshop_input(message):
    """
    Просит ввести названия кофейни
    :param message:
    :return:
    """
    markup = types.InlineKeyboardMarkup()
    bot.send_message(message.from_user.id, 'Введите название кофейни c //', reply_markup=markup)


# @bot.message_handler(content_types=["text"])
# @bot.callback_query_handler(func=lambda message: '//' in message.text)
def search_coffeeshop_output(message: types.Message):
    """
    Возвращает результат поиска
    :param message:
    :return:
    """
    page_controller = SearchCoffeeShopPageController(session)
    markup = types.InlineKeyboardMarkup()
    # markup.add(types.InlineKeyboardButton(switch_inline_query='', text='Coffee'))
    data = page_controller.get_coffeeshop(message.text[2:])
    for coffeeshop in data:
        markup.add(types.InlineKeyboardButton(text=coffeeshop['text'], callback_data=coffeeshop['callback_data']))

    bot.send_message(message.from_user.id, f'Результат поиска по "{message.text[2:]}":', reply_markup=markup)