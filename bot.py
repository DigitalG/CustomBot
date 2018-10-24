import os
from telebot import types
from telebot.types import Message
import telebot
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CustomBot.settings")
import django

django.setup()
from admin_panel.models import *

while not TeleBot.objects.all().exists():
    print('Waiting for bot token')
    time.sleep(3)

TOKEN = ''
#TOKEN = TeleBot.objects.all()[0].token
bot = telebot.TeleBot(TOKEN)
bot_id = bot.get_me().id


def applyFilter(filter: Filter, str):
    if filter.type == 'Replace':
        result = str.replace(filter.input, filter.output)
    elif filter.type == 'Add Below':
        result = str + '\n\n' + filter.input
    elif filter.type == 'Remove':
        result = str.replace(filter.input, '')

    return result


@bot.message_handler(content_types=['text'])
def send_welcome(message: Message):
    f = open('msg.txt', 'r')
    tmp = f.read().split('|||')
    print(tmp)
    bot.send_message(, tmp[0])


bot.polling()

