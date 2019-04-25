import discord
import asyncio
import random
import os
import json

client = discord.Client()
SCORE = {}
KANJI = {}
GUILD_ID = 0
CHANNEL_ID = 0
TIME = 0
rand_list = []
# KANJI_SIZE = 0
cur = ""
async def load():
        print("loading data... ", end="")
        data = json.load(open("data.json","r"))
        config = json.load(open("config.json","r"))
        global KANJI
        global SCORE
        global GUILD_ID
        global CHANNEL_ID
        global TIME
        SCORE = data["score"].copy()
        KANJI = data["kanji"].copy()
        #print(list(KANJI))
        GUILD_ID = config["guild"]
        # print(GUILD_ID)
        CHANNEL_ID = config["channel"]
        TIME = config["time"]
        # KANJI_SIZE = len(KANJI)
        print("done")

async def create_list():
        global rand_list
        for key, val in KANJI.items():
                rand_list += [key]*SCORE[val]

async def save():
        print("saving files...", end="")
        json.dump(SCORE,open("data.json","w"))
        print("done")

async def bgtask():
        global cur
	# channel = client.get_guild(int(GUILD_ID)).get_channel(int(CHANNEL_ID))
        channel = client.guilds[0].channels[1]
        print("initializing background task")
        while True:
                print("fetching a random kanji..."," ")
                sel = random.choice(rand_list)
                await channel.send(sel)
                cur = KANJI[sel]
                print("sent")
                await asyncio.sleep(TIME)

@client.event
async def on_ready():
        await load()
        await create_list()
        # print(KANJI)
        client.loop.create_task(bgtask())

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	else:
                print("answer received!")
                if message.content == cur:
                        message.channel.send("right!")
                        print("right!")
                        print(SCORE)
                        SCORE[cur]-=1
                else:
                        message.channel.send("wrong!")
                        print("wrong!")
print("initializing bot")
client.run(os.environ['TOKEN'])
# client.run(json.load(open("token.json"))["TOKEN"])
