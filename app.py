import telebot

from main import *


@bot.message_handler(content_types=['text'])
def redirect_by_bot(message):
    if message.text == 'Все кофейни в Спб':
        list_coffeeshop(message, 1)
    elif message.text == 'Функции бота':
        description_option_bot(message)
    elif message.text == 'Кофейни рядом':
        user_location(message)
    elif message.text == 'Поиск кофейни':
        search_coffeeshop_input(message)
    elif '//' in message.text:
        search_coffeeshop_output(message)

    print(message)


bot.polling(none_stop=True, interval=0, path_to_watch='/')