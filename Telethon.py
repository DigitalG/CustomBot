from telethon import TelegramClient, events, sync, client
import asyncio
import random
import os

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

client = TelegramClient('session_name', api_id, api_hash)

client.start()

# for dialog in client.get_dialogs(limit=2):
#     for message in client.iter_messages(dialog, limit=1):
#         print(dialog.name, ' text= ' + message.text)


# dialogs = client.get_dialogs('t.me/vape_baraholkaua')
# client.send_message('Korbit',[dialogs])

# print(client.get_me().stringify())

# client.send_message('vasylmartyniv', 'Hello! Talking to you from Telethon')
# client.send_file('username', '/home/myself/Pictures/holidays.jpg')


# #client.get_input_message('DigitalG')
# @client.on(events.NewMessage(pattern='(?i)hi|hello'))
# async def handler(event):
#     await event.respond('Hey!')

@client.on(events.NewMessage)
async def my_event_handler(event):
    if 'бля' in event.raw_text:
        await print(event.message)


client.start()
client.run_until_disconnected()

# client.start()
#
# list = ['хуй','пизда','жопа','соски','ебать ты лох','мразь','нахуй иди']
# while True:
#     client.send_message('DigitalG',random.choice(list))
#
# client.start()
# client.run_until_disconnected()
