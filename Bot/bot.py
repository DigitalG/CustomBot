from telebot import types
from telebot.types import Message
import telebot

t = open('token.txt', 'r')
TOKEN = t.readline()
t.close()

bot = telebot.TeleBot(TOKEN)


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
    kek = 'Replace'
    r = [message.text]
    for i in range(len(r)):
        tmp = r[i].split(' ')
        print(tmp)
    return r
    if kek in message.text:
        bot.send_message(message.chat.id, '#' + message.text)


bot.polling()
