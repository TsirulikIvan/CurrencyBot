import telebot
from urllib.request import urlopen
from xml.etree import ElementTree as ET

API_TOKEN = "937787082:AAFOsK43-3Aq0UpuLYQ8-hFX2edgENzgkmQ"

bot = telebot.TeleBot(API_TOKEN)

my_cur = ['R01239', 'R01235', 'R01035']

def cur_wrapper(currensies):
    res = ''
    for cur in currensies:
        res += '\u2705 Название валюты: {0} ({1})\nТекущий курс: {2};\n'.format(*cur)
    return res


def get_currencies(currencies_ids_lst=my_cur):
    cur_res_str = urlopen("http://www.cbr.ru/scripts/XML_daily.asp")
    result = []
    cur_res_xml = ET.parse(cur_res_str)
    root = cur_res_xml.getroot()
    valutes = root.findall('Valute')
    for el in valutes:
        valute_id = el.get('ID')
        if str(valute_id) in currencies_ids_lst:
            valute_cur_val = el.find('Value').text
            valute_name = el.find('Name').text
            result.append((valute_name, valute_id, valute_cur_val))
    return result

@bot.message_handler(commands=['start'])
def welcome_msg(message):
    bot.send_message(message.chat.id, 'Привет, ты написал /start!\n'
                                      'Я бот который помогает тебе анализировать и узнавать курсы валюты;\n'
                                      'Напиши /help чтоб получить полную справку по функциям')


@bot.message_handler(commands=['help'])
def help_msg(message):
    bot.send_message(message.chat.id, 'Введите /daily чтоб получить сегодняшнее значений курсов валют!\n'
                                      'Введите /currencies чтоб получить список отслеживаемых валют!\n'
                                      'Введите /uniq_cur чтоб перейти к работе с конкретной валютой!\n')

@bot.message_handler(commands=['daily'])
def help_msg(message):
    bot.send_message(message.chat.id, cur_wrapper(get_currencies()))


@bot.message_handler(commands=['currencies'])
def help_msg(message):
    bot.send_message(message.chat.id, 'id отслеживаемых валют: {0}'.format(*my_cur))

@bot.message_handler(commands=['uniq_cur'])
def help_msg(message):
    cur_id = message.text.split(' ')[1]
    bot.send_message(message.chat.id, 'Вы хотите проанализировать валюту c id: {0}?'.format(cur_id))

bot.polling()