import discord
import asyncio
import random
import os
import psycopg2
import json

#c.execute("create table hello (a int, b int)")
#c.execute("update helloworld set a = 2, b = 3")
#conn.commit()
#c.execute("select * from helloworld")
#print(c.fetchall())
client = discord.Client()
channel = discord.abc.GuildChannel()

class Data:

    async def rm(self, key):
        self.score[key] -= 1

    async def add(self, key):
        self.score[key] += 1

    async def save(self):
        for key in self.romaji:
            self.cursor.execute("update kanji set score = %s where kanji = %s", (self.score[key],key))
        self.conn.commit()

    async def _init(self):
        self.romaji = {}
        self.score = {}
        self.conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode = 'require')
        self.cursor = self.conn.cursor()
        self.cursor.execute("select * from kanji", (str,))
        lis = self.cursor.fetchall()
        for tmp in lis:
            self.romaji[tmp[0]] = tmp[1]
            self.score[tmp[0]] = tmp[2]

data = Data()

class Configuration:
    """
    guild_id = 0
    channel_id = 0
    time = 0
    prefix = ""
    """
    async def _init(self, data):
        guild_id = data["guild"]
        channel_id = data["channel"]
        self.time = data["time"]
        self.prefix = data["prefix"]
        self.channel = client.get_guild(guild_id).get_channels(channel_id)

config = Configuration()

class Question:

    async def is_up(self):
        return False if self.current == "" else True

    async def reset(self):
        self.current = ""

    async def verify(self, answer):
        if answer == data.romaji[self.current]:
            await config.channel.send("right!")
            await data.rm(self.current)
            self.rand_list.remove(self.current)
        else:
            await config.channel.send("wrong! The correct answer is " + data.romaji[self.current])
            await data.add(self.current)
            self.rand_list.append(self.current)

    async def _init(self):
        self.rand_list = []
        for key in data.romaji:
            self.rand_list += [key]*data.score[key]
        self.current = random.choice(self.rand_list)
q = Question()

class Command:

    async def command_score(self):
        print("running command")
        await config.channel.send("```prolog\n" + json.dumps(data.score, indent = 2) + "```")

    async def run(self,cmd):
        print("command received")
        method_name = 'command_' + str(cmd)
        method = getattr(self, method_name)
        await method()

async def bgtask():
    while True:
        # print(q.current)
        if q.is_up():
            await asyncio.sleep(config.time)
            continue
        await q._init()
        await config.channel.send("how do you say " + q.current +"?")
        await asyncio.sleep(config.time)


@client.event
async def on_ready():
    await data._init()
    await config._init(json.load(open("config.json", encoding="utf8")))
    #channel = client.guilds[0].channels[1]
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
