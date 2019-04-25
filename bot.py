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
channel = discord.abc.GuildChannel()
cur = ""
# KANJI_SIZE = 0

async def load():
        global KANJI
        global SCORE
        global GUILD_ID
        global CHANNEL_ID
        global TIME
        global channel

        print("loading data... ", end="")

        data = json.load(open("data.json","r"))
        config = json.load(open("config.json","r"))

        channel = client.get_guild(GUILD_ID).get_channel(CHANNEL_ID)
        SCORE = data["score"].copy()
        KANJI = data["kanji"].copy()
        GUILD_ID = config["guild"]
        CHANNEL_ID = config["channel"]
        TIME = config["time"]
        print("done")

async def create_list():
        global rand_list
        for key in KANJI:
                rand_list += [key]*SCORE[key]

async def bgtask():
        global cur
        # channel = client.guilds[0].channels[1]
        print("initializing background task")
        while True:
                print("fetching a random kanji..."," ")
                sel = random.choice(rand_list)
                await channel.send("how do you say " + sel +"?")
                cur = sel
                print("sent")
                await asyncio.sleep(TIME)

async def save():
        print("saving files...", end="")
        json.dump(SCORE,open("data.json","w"))
        print("done")

async def right_ans():
        global cur
        await channel.send("right!")
        # print("right!")
        SCORE[cur]-=1
        print(SCORE)
        rand_list.remove(cur)
        # cur = ""

async def wrong_ans():
        global cur
        await channel.send("wrong! The correct answer is " + KANJI[cur])
        # print("wrong!")
        SCORE[cur]+=1
        print(SCORE)
        rand_list.append(cur)
        # cur = ""

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
                if message.content == KANJI[cur]:
                        await right_ans()
                else:
                        await wrong_ans()
                        
print("initializing bot")
client.run(os.environ['TOKEN'])
# client.run(json.load(open("token.json"))["TOKEN"])
