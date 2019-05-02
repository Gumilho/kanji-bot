import discord
import asyncio
import random
import os
import psycopg2
import json

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode = 'require')
c = conn.cursor()
#c.execute("create table hello (a int, b int)")
#c.execute("update helloworld set a = 2, b = 3")
c.execute("select * from helloworld")
print(c.fetchall())
client = discord.Client()
channel = discord.abc.GuildChannel()
class Data:

    async def rm(self, key):
        self.score[key] -= 1

    async def add(self, key):
        self.score[key] += 1

    async def save(self):
        self.cursor.execute("Update kanji set score = %s where id = %s")

    async def _init(self, data):
        self.cursor = conn.cursor()
        self.cursor.execute("select * from kanji where name = 'romaji'", (str,))
        self.romaji = await self.cursor.fetchall()
        self.cursor.execute("select * from kanji where name = 'score'", (str,))
        self.score = await self.cursor.fetchall()
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
        if answer == data.romaji[self.current]:
            await channel.send("right!")
            await data.rm(self.current)
            self.rand_list.remove(self.current)
        else:
            await channel.send("wrong! The correct answer is " + data.romaji[self.current])
            await data.add(self.current)
            self.rand_list.append(self.current)

    async def _init(self):
        for key in data.romaji:
            self.rand_list += [key]*data.score[key]
        self.current = random.choice(self.rand_list)
q = Question()

class Command:

    async def command_score(self):
        print("running command")
        await channel.send("```prolog\n" + json.dumps(data.score, indent = 2) + "```")

    async def run(self,cmd):
        print("command received")
        method_name = 'command_' + str(cmd)
        method = getattr(self, method_name)
        await method()

async def bgtask():
    while True:
        # print(q.current)
        if not q.current == "":
            await asyncio.sleep(config.time)
            continue
        await q._init()
        await channel.send("how do you say " + q.current +"?")
        await asyncio.sleep(config.time)


@client.event
async def on_ready():
    global channel
    await data._init(json.load(open("data.json", encoding="utf8")))
    await config._init(json.load(open("config.json", encoding="utf8")))
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
