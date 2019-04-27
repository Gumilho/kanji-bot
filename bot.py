import discord
import asyncio
import random
import os
import json

class Data:

    kanji = {}
    score = {}
    
    async def rm(self, key):
        self.score[key] -= 1

    async def add(self, key):
        self.score[key] += 1

    def __init__(self):
        data = json.load(open("data.json","r"))
        self.kanji = data["kanji"]
        self.score = data["score"]
data = Data()

class Configuration:

    guild_id = 0
    channel_id = 0
    time = 0

    def __init__(self):
        print("config started")
        data = json.load(open("config.json","r"))
        self.guild_id = data["guild"]
        print(self.guild_id)
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


    def __init__(self):
        self.rand_list = [key*data.score[key] for key in data.kanji]
        self.current = random.choice(self.rand_list)


client = discord.Client()
print("guild id: " + str(client.guilds))
channel = client.get_guild(config.guild_id).get_channel(config.channel_id)
q = Question()

async def bgtask():
    # channel = client.guilds[0].channels[1]
    print("initializing background task")
    while True:
        q = Question()
        await channel.send("how do you say " + q.current +"?")
        await asyncio.sleep(config.time)

async def save():
    print("saving files...", end="")
    json.dump(data.score,open("data.json","w"))
    print("done")

@client.event
async def on_ready():
    client.loop.create_task(bgtask())

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        print("answer received!")
        await q.verify(message.content)

                        
print("initializing bot")
client.run(os.environ['TOKEN'])
# client.run(json.load(open("token.json"))["TOKEN"])
