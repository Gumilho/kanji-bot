import discord
import asyncio
import random
import os
import json
import config

client = discord.Client()
KANJI = {}
rand_list = []
GUILD_ID = 0
CHANNEL_ID = 0
TIME = 0
cur = ""
# KANJI_SIZE = 0

async def channel():
        return client.get_guild(GUILD_ID).get_channel(CHANNEL_ID)

async def config():
        return json.load(open("config.json","r"))]

async def guild_id():
        return config.guild

async def channel_id():
        return config()["channel"]

async def interval():
        return config()["time"]

async def data():
        return json.load(open("data.json","r"))

async def score():
        dat = await data()
        return await data()["score"]

async def kanji():
        dat = await data()
        return await data()["kanji"]

async def load():
        global KANJI
        global SCORE
        global GUILD_ID
        global CHANNEL_ID
        global TIME
        global channel

        print("loading data... ", end="")

        channel = 
        
        
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
