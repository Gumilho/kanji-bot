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
# KANJI_SIZE = 0
cur = ""
def load():
        print("loading data... ", end="")
        data = json.load(open("data.json","r"))
        config = json.load(open("config.json","r"))
        SCORE = data["score"]
        KANJI = data["kanji"]
        #print(list(KANJI))
        GUILD_ID = config["guild"]
        # print(GUILD_ID)
        CHANNEL_ID = config["channel"]
        TIME = config["time"]
        # KANJI_SIZE = len(KANJI)
        print("done")

async def save():
        print("saving files...", end="")
        json.dump(SCORE,open("data.json","w"))
        print("done")

async def bgtask():
	# channel = client.get_guild(int(GUILD_ID)).get_channel(int(CHANNEL_ID))
        channel = client.guilds[0].channels[1]
        print("initializing background task")
        while True:
                print(list(KANJI))
                sel = random.choice(list(KANJI))
                await channel.send(sel)
                cur = KANJI[sel]
                print(cur)
                await asyncio.sleep(TIME)

@client.event
async def on_ready():
        load()
        client.loop.create_task(bgtask())

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	else:
		await message.channel.send("Hi")
		
print("initializing bot")
client.run(os.environ['TOKEN'])
# client.run(json.load(open("token.json"))["TOKEN"])
