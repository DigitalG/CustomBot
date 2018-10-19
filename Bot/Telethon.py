from telethon import TelegramClient, events, sync
import asyncio

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
lines = []
f = open('info.txt')
lines = f.readlines()
api_id = int(lines[0])
api_hash = lines[1]

client = TelegramClient('session_name', api_id, api_hash)


# print(client.get_me().stringify())

# client.send_message('vasylmartyniv', 'Hello! Talking to you from Telethon')
# client.send_file('username', '/home/myself/Pictures/holidays.jpg')


# #client.get_input_message('DigitalG')
# @client.on(events.NewMessage(pattern='(?i)hi|hello'))
# async def handler(event):
#     await event.respond('Hey!')

@client.on(events.NewMessage)
async def my_event_handler(event):
    if 'правий' in event.raw_text:
        await event.reply('я правий')


client.start()
client.run_until_disconnected()
