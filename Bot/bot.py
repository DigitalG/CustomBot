from telebot import types
from telebot.types import Message
import telebot
from django.db import models
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CustomBot.settings")
from .admin_panel.models import *

t = open('token.txt', 'r')
TOKEN = t.readline()
t.close()

bot = telebot.TeleBot(TOKEN)


def applyFilter(filter: Filter, str):
    if filter.type == 'Replace':
        result = str.replace(filter.input, filter.output)
    elif filter.type == 'Add Below':
        result = str + '\n\n' + filter.input
    elif filter.type == 'Remove':
        result = str.replace(filter.input, '')

    return result


@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    bot.send_message(message.chat.id,
                     'Hello, {}, this bot will format your message for posting'.format(str(message.chat.first_name)))


t = open('examples.txt', 'r')
examples = t.read()
t.close()


@bot.message_handler(commands=['examples'])
def send_welcome(message: Message):
    bot.send_message(message.chat.id, examples)


@bot.message_handler(commands=['help'])
def send_welcome(message: Message):
    bot.send_message(message.chat.id,
                     'This bot can format your forwarded message, you can send me /examples command to see it')


@bot.message_handler(func=lambda m: True)
@bot.edited_message_handler(func=lambda m: True)
def add_tags(message):
    # kek = 'Replace'
    # r = [message.text]
    # for i in range(len(r)):
    #     tmp = r[i].split(' ')
    #     print(tmp)
    # return r
    # if kek in message.text:
    #     bot.send_message(message.chat.id, '#' + message.text)

    answer = message.text
    filters = Filter.objects.all()
    for f in filters:
        answer = applyFilter(answer, f)

    bot.send_message(message.chat.id, answer)


bot.polling()
