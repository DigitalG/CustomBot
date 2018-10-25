from telethon import TelegramClient, events, sync, client
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

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.


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
#             client.download_profile_photo(phone_number,'admin_panel/static/img/profile')
#
# myself = client.get_entity(phone_number)
# client.download_profile_photo(myself,'admin_panel/static/img/profile')

client_id = client.get_entity(phone_number)
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
    channels = Channel.objects.all()
    res = []
    for c in channels:
        res.append(c.key)
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
    # await print(str)
    # get_filters(id)
    # print(get_filters(id))
    # print(event.message.to_id.user_id)
    await client.send_message(bot_id, '***')


# @client.on(events.NewMessage(chats=['DigitalG', 'Korb1t']))
# def my_event_handler(event):
#     id = event.message.id
#     # filters =
#     print(Channel.objects.filter(key=create_dictionary()[id]).filters)
#     if '' in event.raw_text:
#         client.send_message('DigitalG', 'kughu')


# client.start()
# print(Channel.objects.filter(key=create_dictionary()['340934389'])[0].filters.all())
# print(dic)
client.run_until_disconnected()

'''dialogs = client.get_dialogs('t.me/vape_baraholkaua')
client.send_message('Korbit',[dialogs])

print(client.get_me().stringify())

client.send_message('vasylmartyniv', 'Hello! Talking to you from Telethon')
client.send_file('username', '/home/myself/Pictures/holidays.jpg')

for dialog in client.get_dialogs(limit=2):
    for message in client.iter_messages(dialog, limit=1):
        print(dialog.name, ' text= ' + message.text)

#client.get_input_message('DigitalG')
@client.on(events.NewMessage(pattern='(?i)hi|hello'))
async def handler(event):
    await event.respond('Hey!')
client.start()

list = ['хуй','пизда','жопа','соски','ебать ты лох','мразь','нахуй иди']
while True:
    client.send_message('DigitalG',random.choice(list))

client.start()
client.run_until_disconnected()'''
