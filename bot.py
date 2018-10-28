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

TOKEN = TeleBot.objects.all()[0].token
bot = telebot.TeleBot(TOKEN)
bot_id = bot.get_me().id
client_id = Session.objects.all()[0].self_id
print('>>>Debug: Start')


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
    f = open('dic.txt', 'r')
    dic = parse_dictionary()
    tmp = f.read().split(';')
    print(message)
    if message.forward_from_chat:
        key = dic[str(message.forward_from_chat.id).replace('-100', '')]
        title = message.forward_from_chat.title
    elif message.chat:
        key = dic[str(message.chat.id).replace('-', '')]
        title = message.chat.title
    elif message.forward_from:
        key = dic[str(message.forward_from.id)]
        title = message.forward_from.username
    text = message.text
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
            text = 'Forwarded from @{}: \n  {}'.format(title, text)
        bot.send_message(client_id, text)


@bot.message_handler(content_types=['photo'])
def handle_docs_audio(message):
    f = open('dic.txt', 'r')
    dic = parse_dictionary()
    tmp = f.read().split(';')
    print(message)
    if message.forward_from_chat:
        key = dic[str(message.forward_from_chat.id).replace('-100', '')]
        title = message.forward_from_chat.title
    elif message.chat:
        key = dic[str(message.chat.id).replace('-', '')]
        title = message.chat.title
    elif message.forward_from:
        key = dic[str(message.forward_from.id)]
        title = message.forward_from.username
    text = message.text
    try:
        channel = Channel.objects.get(key=key)
    except Channel.DoesNotExist:
        return

    caption = ''
    part = ''
    try:
        if message.json['caption']:
            part = message.json['caption']
    except KeyError:
        part = ''
    if channel.forfilter == 'Only Images':
        caption = ''
        bot.send_photo(client_id, message.json['photo'][0]['file_id'], caption=caption)
    if channel.forfilter == 'Only messages that include an image':
        caption = 'Forwarded from {}\n\n{}'.format(title, part)
        bot.send_photo(client_id, message.json['photo'][0]['file_id'], caption=caption)
    if channel.forfilter == 'Only Text':
        bot.send_message(client_id, caption)
    if channel.forfilter == 'Only messages that include an text' and message.json['caption']:
        caption = 'Forwarded from {}\n\n{}'.format(title, part)
        bot.send_photo(client_id, message.json['photo'][0]['file_id'], caption=caption)
    if channel.forfilter == 'Everything':
        caption = 'Forwarded from {}\n\n{}'.format(title, part)
        bot.send_photo(client_id, message.json['photo'][0]['file_id'], caption=caption)


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
