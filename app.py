import telebot

from main import *


@bot.message_handler(content_types=['text'])
def redirect_by_bot(message):
    if message.text == 'Все кофейни в Спб':
        list_coffeeshop(message)
    elif message.text == 'Функции бота':
        description_option_bot(message)
    elif message.text == 'Кофейни рядом':
        user_location(message)

    print(message)


bot.polling(none_stop=True, interval=0, path_to_watch='/')