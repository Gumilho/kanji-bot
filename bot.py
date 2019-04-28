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

    async def save(self):
        data = {}
        data['score'] = self.score
        data['kanji'] = self.kanji
        f = open("data.json","w"),
        f.write(json.dumps(data, indent=4))
        print("saved!")
        f.close()

    async def _init(self, data):
        self.kanji = data["kanji"]
        self.score = data["score"]
data = Data()

class Configuration:
    """
    guild_id = 0
    channel_id = 0
    time = 0
    prefix = ""
    """
    async def _init(self, data):
        self.guild_id = data["guild"]
        self.channel_id = data["channel"]
        self.time = data["time"]
        self.prefix = data["prefix"]
config = Configuration()

class Question:

    current = ""
    rand_list = []
    
    async def is_up(self):
        return False if self.current == "" else True

    async def reset(self):
        self.current = ""

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

class Command:

    async def command_score(self):
        print("running command")
        await channel.send(data.score)

    async def run(self,cmd):
        print("command received")
        method_name = 'command_' + str(cmd)
        method = getattr(self, method_name)
        await method()

async def bgtask():
    # channel = client.guilds[0].channels[1]
    print("initializing background task")
    while True:
        await q._init()
        await channel.send("how do you say " + q.current +"?")
        await asyncio.sleep(config.time)


@client.event
async def on_ready():
    global channel
    await data._init(json.load(open("data.json", encoding="utf8")))
    await config._init(json.load(open("config.json", encoding="utf8")))
    print(client.guilds)
    print(config.guild_id)
    channel = client.guilds[0].channels[1]
    client.loop.create_task(bgtask())

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        if message.content.startswith(config.prefix):
            c = Command()
            await c.run(message.content[1:])
        else:
            print("answer received!")
            await q.verify(message.content)
            await q.reset()
            await data.save()
                        
print("initializing bot")
client.run(os.environ['TOKEN'])

