import discord
import asyncio
import random
import os
import json

client = discord.Client()
SCORE = []
KANJI = {}
GUILD_ID = 0
CHANNEL_ID = 0
TIME = 0
CONFIG = {}
async def load():
        print("loading files...", end="")
        data = json.load(open("data.json","r"))
        config = json.load(open("config.json","r"))
        SCORE = data["score"]
        KANJI = data["kanji"]
        GUILD_ID = config["guild"]
        CHANNEL_ID = config["channel"]
        TIME = config["time"]
        print("done")

async def save():
        print("saving files...", end="")
        json.dump(SCORE,open("data.json","w"))
        print("done")

async def bgtask():
	channel = client.get_guild(GUILD_ID).get_channel(CHANNEL_ID)
	while True:
		await channel.send(random.choice(KANJI))
		await asyncio.sleep(TIME)

@client.event
async def on_ready():
        await load()
        client.loop.create_task(bgtask())

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	else:
		await message.channel.send("Hi")
		
client.run(os.environ['TOKEN'])
# client.run(json.load(open("token.json"))["TOKEN"])
