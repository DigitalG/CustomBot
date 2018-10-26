from telethon import TelegramClient, events, sync, client
from telethon.tl.types import PeerUser, PeerChannel
import asyncio
import random
import os
from telebot import types
from telebot.types import Message
import telebot
import asgiref
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CustomBot.settings")
import django

django.setup()
from admin_panel.models import *

TOKEN = TeleBot.objects.all()[0].token
bot = telebot.TeleBot(TOKEN)
bot_id = bot.get_me().id

lines = []
f = open('info.txt')
lines = f.readlines()
api_id = int(lines[0])
api_hash = lines[1]

phone_number = None
code = '0'
while not phone_number:
    time.sleep(3)
    print('waiting for phone number')
    if Session.objects.all().exists():
        phone_number = Session.objects.all()[0].number
if phone_number:
    client = TelegramClient('s2', api_id, api_hash)
    client.connect()
    if not client.is_user_authorized():
        if code == '0':
            client.send_code_request(phone_number)
            while (code == '0'):
                code = str(Session.objects.all()[0].code)
                time.sleep(3)
                print('waiting for code...')
            client.sign_in(phone_number, code)

to_edit = Session.objects.all()[0]
to_edit.self_id = client.get_me().id
to_edit.save()

client.get_dialogs()
client_id = client.get_entity(phone_number)
bot_entity = client.get_entity(bot_id)
print('>>>Debug:Bot Started')


def applyFilter(str, filter):
    result = str
    if filter.type == 'Replace':
        result = result.replace(filter.input, filter.output)
    elif filter.type == 'Add Below':
        result = result + '\n\n' + filter.input
    elif filter.type == 'Remove':
        result = result.replace(filter.input, '')

    return result


def dic_check(key):
    f = open('dic.txt', 'r+')
    tmp = f.readlines()
    for r in tmp:
        str = r.split(';')
        dic[str[0]] = str[1]
    if key not in dic:
        dic[key] = client.get_entity(key).id
        f.write('{};{}'.format(key, client.get_entity(key)))


def parse_channels():
    channels = Channel.objects.all()
    res = []
    for c in channels:
        res.append(client.get_entity(c.key))
    return res


def parse_channels_names():
    f = open('dic.txt', 'r+')
    tmp = f.readlines()
    dic = {}
    for r in tmp:
        str = r.split(';')
        dic[str[0]] = str[1]
    channels = Channel.objects.all()
    res = []
    for c in channels:
        res.append(c.key)
        if c.key not in dic:
            dic[c.key] = client.get_entity(c.key).id
            f.write('{};{}\n'.format(c.key, client.get_entity(c.key).id))

    return res


def prepare_message(str, id):
    return applyFilter(str, id)


def get_filters(id):
    id = str(id)
    return Channel.objects.filter(key=create_dictionary()[str(id)])[0].filters.all()


id = None
str_to_send = ''


@client.on(events.NewMessage(chats=parse_channels_names()))
async def my_event_handler(event):
    if event.message.from_id:
        id = event.message.from_id
    else:
        id = event.message.to_id.channel_id
    str_to_send = event.message.text
    print('{} send to {}'.format(str_to_send, str(id)))
    f = open('msg.txt', 'w')
    f.write('{}|||{}'.format(str_to_send, id))
    message = await client.forward_messages(bot_entity, event.message)
    await asyncio.sleep(1)
    await message.delete()


client.run_until_disconnected()
