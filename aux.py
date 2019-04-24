import discord
import asyncio
import random
import os
import json

client = discord.Client()
KANJI = ["楽しい","嬉しい"]
async def bgtask():
    channel = client.get_guild(int("493580129025654785")).get_channel(int("493580129025654787"))
    print(channel)
    while True:
        await channel.send(random.choice(KANJI))
        await asyncio.sleep(20)

@client.event
async def on_ready():
        print("dois")
        print(client.guilds)
        client.loop.create_task(bgtask())

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	else:
		await message.channel.send("Hi")
		
# client.run(os.environ['TOKEN'])
client.run("NTY5NTY0NjcwODg5ODIwMTYw.XMB2ng.ZLi6y5KNl9j9Zt1BhpyHneNzDWU")
