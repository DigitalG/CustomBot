import os
from telebot import types
from telebot.types import Message
import telebot
import time
from telethon import TelegramClient, events, sync, client
import asyncio

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CustomBot.settings")
import django

django.setup()
from admin_panel.models import *

while not TeleBot.objects.all().exists():
    print('Waiting for bot token')
    time.sleep(3)

TOKEN = TeleBot.objects.all()[0].token
bot = telebot.TeleBot(TOKEN)
bot_id = bot.get_me().id
client_id = Session.objects.all()[0].self_id
print('>>>Debug: Start')

lines = []
f = open('info.txt')
lines = f.readlines()
api_id = int(lines[0])
api_hash = lines[1]
client = TelegramClient('s2', api_id, api_hash)
client.connect()


def applyFilter(filter: Filter, str):
    if filter.type == 'Replace':
        result = str.replace(filter.input.lower(), filter.output)
        result = result.replace(filter.input, filter.output)
        result = result.replace(filter.input.upper(), filter.output)
    elif filter.type == 'Add Below':
        result = str + '\n\n' + filter.input
    elif filter.type == 'Remove':
        result = str.replace(filter.input, '')
        result = result.replace(filter.input.upper(), '')
        result = result.replace(filter.input.lower(), '')

    return result


def parse_dictionary():
    f = open('dic.txt', 'r')
    tmp = f.readlines()
    res = {}
    for s in tmp:
        t = s.replace('\n', '').split(';')
        res[t[1]] = t[0]

    return res


@bot.edited_message_handler(content_types=['text'])
@bot.message_handler(content_types=['text'])
def send_text(message: Message):
    f = open('dic.txt', 'r')
    dic = parse_dictionary()
    tmp = f.read().split(';')
    key = dic[str(message.forward_from.id)]
    text = message.text
    channel = Channel.objects.get(key=key)
    if not channel.forfilter == 'Only messages that include an image':
        for fl in channel.filters.all():
            text = applyFilter(fl, text)
        if channel.KeepForwardedCaption:
            text = 'Forwarded from @{}: \n  {}'.format(message.forward_from.username, text)
        bot.send_message(client_id, text)


@bot.message_handler(content_types=['photo'])
def handle_docs_audio(message):
    f = open('dic.txt', 'r')
    dic = parse_dictionary()
    tmp = f.read().split(';')
    key = dic[str(message.from_user.id)]
    text = message.text
    channel = Channel.objects.get(key=key)
    caption = message.json['caption']
    if channel.forfilter == 'Only Images':
        caption = ''
        bot.send_photo(client_id, message.json['photo'][0]['file_id'], caption=caption)
    if channel.forfilter == 'Only messages that include an image':
        caption = message.json['caption']
        bot.send_photo(client_id, message.json['photo'][0]['file_id'], caption=caption)
    if channel.forfilter == 'Only Text':
        bot.send_message(client_id, caption)


@bot.message_handler(content_types=['video'])
def handle_docs_video(message):
    bot.send_video(client_id, message.json['video']['file_id'], caption=message.json['caption'])


@bot.message_handler(content_types=['audio'])
def handle_docs_video(message):
    bot.send_audio(client_id, message.json['audio']['file_id'])


@bot.message_handler(content_types=['document'])
def handle_docs_video(message):
    bot.send_document(client_id, message.json['document']['file_id'])


bot.polling()
