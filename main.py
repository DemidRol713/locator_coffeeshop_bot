import telebot
from telebot import types

import config

bot = telebot.TeleBot(config.tg_token)


@bot.message_handler(commands=['start'])
def start(message):

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Привет! Я бот-помощник в поиске кофейн поблизости!", reply_markup=markup)


@bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.InlineKeyboardMarkup()
    btn_description = types.InlineKeyboardButton(text='Описание бота', callback_data='description')
    markup.add(btn_description)

    bot.send_message(message.from_user.id, "Что нужно?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def options(call):
    if call.data == 'description':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        bot.send_message(call.from_user.id, "Должно быть описание, но пока нет!", reply_markup=markup)


@bot.message_handler(commands=['list_all_coffeeshop'])
def list_all_coffeeshop(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu = types.KeyboardButton('Вернуться на главную')
    markup.add(menu)

    bot.send_message(message.from_user.id, "Что нужно?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'description')
def coffeeshop_data(call):
    pass


bot.polling(none_stop=True, interval=0)
