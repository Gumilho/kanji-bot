import discord
import asyncio
import random
import os
import json

client = discord.Client()
channel = discord.abc.GuildChannel()

class Data:

    kanji = {}
    score = {}
    
    async def rm(self, key):
        self.score[key] -= 1

    async def add(self, key):
        self.score[key] += 1

    async def _init(self, data):
        self.kanji = data["kanji"]
        self.score = data["score"]
data = Data()

class Configuration:

    guild_id = 0
    channel_id = 0
    time = 0

    async def _init(self, data):
        self.guild_id = data["guild"]
        print(client)
        self.channel_id = data["channel"]
        self.time = data["time"]


config = Configuration()

class Question:

    current = ""
    verdict = ""
    rand_list = []

    async def verify(self, answer):
        if answer == data.kanji[self.current]:
            await channel.send("right!")
            await data.rm(self.current)
            self.rand_list.remove(self.current)
        else:
            await channel.send("wrong! The correct answer is " + data.kanji[self.current])
            await data.add(self.current)
            self.rand_list.append(self.current)

    async def _init(self):
        for key in data.kanji:
            self.rand_list += [key]*data.score[key]
        self.current = random.choice(self.rand_list)
q = Question()

async def bgtask():
    # channel = client.guilds[0].channels[1]
    print("initializing background task")
    while True:
        await q._init()
        await channel.send("how do you say " + q.current +"?")
        await asyncio.sleep(config.time)

async def save():
    print("saving files...", end="")
    json.dump(data.score,open("data.json","w"))
    print("done")

@client.event
async def on_ready():
    print("ready!")
    global channel
    await data._init(json.load(open("data.json", encoding="utf8")))
    await config._init(json.load(open("config.json", encoding="utf8")))
    print(client.guilds)
    print(config.guild_id)
    channel = client.guilds[0].channels[1]
    client.loop.create_task(bgtask())

@client.event
async def on_message(message):
    print("ready!")
    if message.author == client.user:
        return
    else:
        print("answer received!")
        await q.verify(message.content)

                        
print("initializing bot")
client.run(os.environ['TOKEN'])

