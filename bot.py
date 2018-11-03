import os
from telebot import types
from telebot.types import Message
import telebot
import time
import asyncio

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CustomBot.settings")
import django

django.setup()
from admin_panel.models import *

while not TeleBot.objects.all().exists():
    print('Waiting for bot token')
    time.sleep(3)

while not Session.objects.all().exists():
    print('Waithing for login')
    time.sleep(3)

TOKEN = TeleBot.objects.all()[0].token
client_id = Session.objects.all()[0].self_id
bot = telebot.TeleBot(TOKEN)
bot_id = bot.get_me().id
print('>>>Debug: Start')


def get_ids():
    f = open('admins.txt','r')
    lines = f.readlines()
    res = []
    for l in lines:
        res.append(int(l.replace('\n','').split(';')[1]))
    return res


def applyFilter(filter: Filter, str):
    if filter.type == 'Replace':
        result = str.replace(filter.input.lower(), filter.output)
        result = result.replace(filter.input, filter.output)
        result = result.replace(filter.input.upper(), filter.output)
    elif filter.type == 'Add Below':
        result = str + '\n' + filter.input
    elif filter.type == 'Remove':
        result = str.replace(filter.input, '')
        result = result.replace(filter.input.upper(), '')
        result = result.replace(filter.input.lower(), '')
    elif filter.type == 'If {Input} spotted add {Output} below':
        if filter.input in str or filter.input.lower() in str or filter.input.upper() in str:
            result = str + '\n' + filter.output

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
    text = message.text
    f = open('msg.txt','r')
    arr = []
    arr = f.read().split(';')
    try:
        key = arr[0]
        id = arr[1]
        title = arr[2]
    except IndexError:
        return

    try:
        channel = Channel.objects.get(key=key)
    except Channel.DoesNotExist:
        return
    if not channel.forfilter == 'Only messages that include an image':
        for fl in channel.filters.all():
            if fl.type == 'Get messages only from {Input} username':
                if message.from_user.username != fl.input:
                    return
            else:
                text = applyFilter(fl, text)
        if channel.KeepForwardedCaption:
            text = 'Forwarded from @{}: \n{}'.format(title, text)
        for id in get_ids():
            bot.send_message(id, text)


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    f = open('msg.txt','r')
    arr = []
    arr = f.read().split(';')
    try:
        key = arr[0]
        id = arr[1]
        title = arr[2]
    except IndexError:
        return

    try:
        channel = Channel.objects.get(key=key)
    except Channel.DoesNotExist:
        return
    try:
        if message.json['caption']:
            text = message.json['caption']
    except KeyError:
        text = ''

    for fl in channel.filters.all():
        if fl.type == 'Get messages only from {Input} username':
            if message.from_user.username != fl.input:
                return
        else:
            text = applyFilter(fl, text)
    if channel.KeepForwardedCaption:
        caption = '{}\n\nForwarded from {}'.format(text, title)

    for id in get_ids():
        if channel.forfilter == 'Only Images':
            caption = ''
            bot.send_photo(id, message.json['photo'][0]['file_id'], caption=caption)
        if channel.forfilter == 'Only messages that include an image':
            bot.send_photo(id, message.json['photo'][0]['file_id'], caption=caption)
        if channel.forfilter == 'Only Text':
            bot.send_message(id, caption)
        if channel.forfilter == 'Only messages that include an text' and message.json['caption']:
            bot.send_photo(id, message.json['photo'][0]['file_id'], caption=caption)
        if channel.forfilter == 'Everything':
            bot.send_photo(id, message.json['photo'][0]['file_id'], caption=caption)


@bot.message_handler(content_types=['video'])
def handle_docs_video(message):
    for id in get_ids():
        bot.send_video(id, message.json['video']['file_id'], caption=message.json['caption'])


@bot.message_handler(content_types=['audio'])
def handle_docs_video(message):
    for id in get_ids():
        bot.send_audio(id, message.json['audio']['file_id'])


@bot.message_handler(content_types=['document'])
def handle_docs_video(message):
    for id in get_ids():
        bot.send_document(id, message.json['document']['file_id'])


bot.polling()
