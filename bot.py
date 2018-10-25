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

#TOKEN = '510631047:AAH-SzsULp-731qzkJ2jbizC_rbTyIqt9ww'
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
        result = str.replace(filter.input, filter.output)
    elif filter.type == 'Add Below':
        result = str + '\n\n' + filter.input
    elif filter.type == 'Remove':
        result = str.replace(filter.input, '')

    return result

async def get_id(key):
    return await client.get_entity(key)

async def create_dictionary():
    res = {}
    tmp = None
    channels = Channel.objects.all()
    for c in channels:
        id = await get_id(c.key)
        res[str(id.id)] = str(c.key)

    return res


@bot.message_handler(content_types=['text'])
def send_welcome(message: Message):
    f = open('msg.txt', 'r')
    tmp = f.read().split('|||')
    msg = tmp[0]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(create_dictionary())
    key = result[str(tmp[1])]
    print(Channel.objects.get(key=key).filters)
    for f in Channel.objects.get(key=tmp[1]).filters:
        msg = applyFilter(f,msg)
    bot.send_message(client_id, msg)


bot.polling()
