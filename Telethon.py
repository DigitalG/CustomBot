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

#TODO 2FA
#TODO css footer
#TODO bigalka deletu
#TODO titles homepage
#TODO 404 skeleton tan4ik
#TODO fix supergroup forward
#TODO fix keys (don`t restart telethon)
#TODO STRESS TEST
#TODO STRESS TEST
#TODO STRESS TEST
#TODO STRESS TEST
#TODO STRESS TEST
#TODO STRESS TEST
#TODO STRESS TEST
#TODO STRESS TEST
#TODO STRESS TEST
#TODO STRESS TEST


while not TeleBot.objects.all().exists():
    print('Waiting for bot token')
    time.sleep(3)
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
    client = TelegramClient(phone_number, api_id, api_hash)
    client.connect()
    if not client.is_user_authorized():
        if code == '0':
            client.send_code_request(phone_number)
            while (code == '0'):
                code = str(Session.objects.all()[0].code)
                time.sleep(3)
                print('waiting for code...')
            Session.objects.all()[0].code = '0'
            Session.objects.all()[0].save()

            client.sign_in(phone_number, code)

to_edit = Session.objects.all()[0]
to_edit.self_id = client.get_me().id
to_edit.save()

dialogs = client.get_dialogs()
ent = client.get_entity('DigitalG')
# print(ent.chat.title)
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


#@client.on(events.NewMessage(chats=parse_channels_names()))
@client.on(events.NewMessage)
async def my_event_handler(event):
    msg=False
    # print(event.chat.title)
    # print(event.chat.username)
    try:
        id = event.message.to_id.channel_id
    except AttributeError:
        id = event.message.from_id

    try:
        title = event._chat.title
    except AttributeError:
        ent = await client.get_entity(id)
        title = ent.first_name

    #id = await client.get_input_entity(event.chat.username)
    # id = id.channel_id
    f = open('channels.txt','r')
    tmp = f.readlines()
    #dialogs = await client.get_dialogs()
    for r in tmp:
        r = r.replace('\n', '')
        #ch = await client.get_input_entity(r)
        ch = None
        ch = await client.get_entity(r)
        # print(ch)
        ch_id = ch.id
        if id == ch_id:
            msg = True
            # title = event._chat.title
            f = open('msg.txt', 'w')
            f.write('{};{};{}'.format(r,id,title))
            f.close
            print('ljsdh')
            break
    f.close
    if msg:
        message = await client.forward_messages(bot_entity, event.message)
        await asyncio.sleep(3)
        await message.delete()
    # print('{} send from {}'.format(str_to_send, str(id)))
    # f = open('msg.txt', 'w')
    # f.write('{}|||{}'.format(str_to_send, id))
    #print(message.stringify())

client.run_until_disconnected()


