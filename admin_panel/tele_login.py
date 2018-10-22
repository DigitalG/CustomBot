from telethon import TelegramClient, events, sync, client


def try_login(number, name):
    lines = []
    f = open('info.txt')
    lines = f.readlines()
    api_id = int(lines[0])
    api_hash = lines[1]

    client = TelegramClient(name, api_id, api_hash)
