from telethon import TelegramClient, events, sync, client
import asyncio
import random
import os
from telebot import types
from telebot.types import Message
import telebot

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CustomBot.settings")
import django

django.setup()
from admin_panel.models import *

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
t = open('token.txt', 'r')
TOKEN = t.readline()
t.close()

bot = telebot.TeleBot(TOKEN)

lines = []
f = open('info.txt')
lines = f.readlines()
api_id = int(lines[0])
api_hash = lines[1]

client = TelegramClient('session_name', api_id, api_hash)


def applyFilter(str, channel):
    result = str
    for f in channel.filters:
        if filter.type == 'Replace':
            result = result.replace(filter.input, filter.output)
        elif filter.type == 'Add Below':
            result = result + '\n\n' + filter.input
        elif filter.type == 'Remove':
            result = result.replace(filter.input, '')

    return result


def create_dictionary():
    res = []
    tmp = None
    channels = Channel.objects.all()
    for c in channels:
        tmp = {c.key: client.get_entity(c.key).id}
        res.append(tmp)

    return res


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

def get_filters(id):
    return Channel.objects.filter(key=create_dictionary()[id])[0].filter



@bot.message_handler(func=lambda m: True)
@client.on(events.NewMessage(chats=parse_channels_names()))
async def my_event_handler(event):
    if event.message.from_id:
        id = event.message.from_id
    else:
        id = event.message.to_id.channel_id
    print(event)
    #print(get_filters(id))
    await bot.send_message(id, event.message.text)


print(parse_channels_names())


# @client.on(events.NewMessage(chats=['DigitalG', 'Korb1t']))
# def my_event_handler(event):
#     id = event.message.id
#     # filters =
#     print(Channel.objects.filter(key=create_dictionary()[id]).filters)
#     if '' in event.raw_text:
#         client.send_message('DigitalG', 'kughu')


client.start()
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
