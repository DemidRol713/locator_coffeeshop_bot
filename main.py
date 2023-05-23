import telebot
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from telebot import types
import logging

import config
from model.coffeeshop import CoffeeShop
from service.coffeeshop_service import CoffeeShopService

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
def list_all_coffeeshop(message):
    """
    Список всех кофеен в базе данных
    :param message:
    :return:
    """
    markup = types.InlineKeyboardMarkup()
    coffeeshop_list = session.query(CoffeeShop).limit(10)
    for coffeeshop in coffeeshop_list:
        markup.add(types.InlineKeyboardButton(text=coffeeshop.name, callback_data='coffeeshop_{id}'.format(id=coffeeshop.id)))

    bot.send_message(message.from_user.id, "Что нужно?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: 'coffeeshop' in call.data)
def coffeeshop_card(call):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    coffeeshop_id = int(call.data.split('_')[-1])
    coffeeshop = session.query(CoffeeShop).get(coffeeshop_id)
    text = 'Описание:\n {description}\nАдрес:\n {address}\nСоц.сети и сайты:\n'.format(
        description=coffeeshop.description,
        address=coffeeshop.address
    )
    for website in coffeeshop.website:
        text += website + '\n'

    bot.send_message(call.from_user.id, text, reply_markup=markup)
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
    service = CoffeeShopService(session)
    markup = types.InlineKeyboardMarkup()
    bot.send_message(message.from_user.id, 'Идет поиск кофеен по близости', reply_markup=get_menu_btn(types.ReplyKeyboardMarkup()))

    # data = service.get_coffeeshop_nearby(message.location.latitude, message.location.longitude)
    data = service.get_coffeeshop_nearby(60.016208, 30.372300)
    for coffeeshop in data:
        text = '{name}  {distance} км'.format(
            name=coffeeshop.name,
            distance=coffeeshop.distance
        )
        markup.add(types.InlineKeyboardButton(text=text, callback_data=f'coffeeshop_{coffeeshop.id}'))

    bot.send_message(message.from_user.id, 'В радиусе 2 км:', reply_markup=markup)
