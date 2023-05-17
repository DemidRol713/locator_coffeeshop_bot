import telebot
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from telebot import types

import config
from database.model import CoffeeShop

bot = telebot.TeleBot(config.TG_TOKEN)
engine = create_engine(config.DATA_BASE)
session = Session(bind=engine)


@bot.message_handler(commands=['start'])
def start(message):

    markup = types.InlineKeyboardMarkup()
    bot.send_message(message.from_user.id, "👋 Привет! Я бот-помощник в поиске кофейн поблизости!", reply_markup=markup)


@bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.InlineKeyboardMarkup()
    btn_description = types.InlineKeyboardButton(text='Описание бота', callback_data='description')
    btn_coffee_shop_nearby = types.InlineKeyboardButton(text='Кофейни рядом', callback_data='coffee_shop_nearby')
    markup.add(btn_description)
    markup.add(btn_coffee_shop_nearby)

    bot.send_message(message.from_user.id, "Что нужно?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'description')
def descriptions_option_bot(call):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    bot.send_message(call.from_user.id, "Должно быть описание, но пока нет!", reply_markup=markup)


@bot.message_handler(commands=['list_all_coffeeshop'])
def list_all_coffeeshop(message):
    markup = types.InlineKeyboardMarkup()
    coffeeshop_list = session.query(CoffeeShop).limit(10)
    for coffeeshop in coffeeshop_list:
        markup.add(types.InlineKeyboardButton(text=coffeeshop.name, callback_data='coffeeshop_{id}'.format(id=coffeeshop.id)))

    bot.send_message(message.from_user.id, "Что нужно?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: 'coffeeshop' in call.data)
def description_option_bot(call):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    coffeeshop_id = int(call.data.split('_')[-1])
    coffeeshop = session.query(CoffeeShop).get(coffeeshop_id)
    bot.send_message(call.from_user.id, coffeeshop.description, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: 'coffee_shop_nearby' in call.data)
def coffee_shop_nearby(call):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    geolocation = types.KeyboardButton('Отправить координаты', request_location=True)
    markup.add(geolocation)
    print(geolocation)
    bot.send_message(call.from_user.id, 'Отправьте ваши координаты', reply_markup=markup)


@bot.message_handler(content_types=['location'])
def geolocation_message(message):
    print(message)


bot.polling(none_stop=True, interval=0)
