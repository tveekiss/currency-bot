import telebot
from config import currencies, TOKEN
from extensions import Converter, APIException


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = ('Для начала работы, нужно вести команду боту в следующем формате:'
            '\n<имя валюты, цену которой вы хотите узнать> <имя валюты, в которой надо узнать цену первой валюты> '
            '<количество первой валюты>'
            '\nдля того что бы узнать список доступных валют, введите: /values')
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def start(message: telebot.types.Message):
    text = 'Список доступных валют:'
    for currency in currencies.keys():
        text += f'\n{currency}'
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def main_func(message: telebot.types.Message):
    value = message.text.split(' ')
    try:
        if len(value) != 3:
            raise APIException('Данных должно быть 3')

        quote, base, amount = value
        convert_base = Converter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {convert_base}'
        bot.send_message(message.chat.id, text)


bot.polling(non_stop=True)
