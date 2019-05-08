
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
#channel = discord.abc.GuildChannel()

class Data:

    async def save(self):
        for user in users 
        for key in self.romaji:
            self.cursor.execute("update %s set score = %s where kanji = %s", (self.score[key],key))
        self.conn.commit()
    def select_table(self, name):
        self.cursor.execute("select * from %s", (name,))
    def check_if_exist(self, name):
        self.cursor.execute("select exists (select * from information_schema.tables where table_name = %s)", (name,))
        return self.cursor.fetchone()[0]

    def __init__(self, name):
        self.conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode = 'require')
        self.cursor = self.conn.cursor()
        if check_if_exist(name)
            self.cursor.execute("select * from %s", (name,))
            lis = self.cursor.fetchall()
            self.romaji = {}
            self.score = {}
            for tmp in lis:
                self.romaji[tmp[0]] = tmp[1]
                self.score[tmp[0]] = tmp[2]
        else:
            create_new_table()

class User:

    async def rm(self, key):                            self.score[key] -= 1                                                                        async def add(self, key):
        self.score[key] += 1

    def __init__(self, member):
        self.id = member.id
        self.name = member.name 
        data = Data(self.name)
        self.score = data.score
        self.can_answer = True

users = []

class Configuration:
    async def _init(self, data):
        guild_id = data["guild"]
        channel_id = data["channel"]
        self.time = data["time"]
        self.prefix = data["prefix"]
        self.channel = client.get_guild(guild_id).get_channels(channel_id)

config = Configuration()

class Question:

    async def reset(self):
        for user in Users
        user.can_answer = True
        self.current = ""

    async def verify(self, answer, user):
        if not user.can_answer:
            continue
        if answer == self.right_answer:
            await config.channel.send("right!")
            await user.rm(self.current)
            self.rand_list.remove(self.current)
            user.can_answer = False
        else:
            await config.channel.send("wrong! The correct answer is " + self.right_answer)
            await user.add(self.current)
            self.rand_list.append(self.current)
            user.can_answer = False

    async def create_list(self):
        for user in users
            for key, values in user.data.score.items():
                self.rand_list += [key]*values
        self.current = random.choice(self.rand_list)
        self.right_answer = users[0].data.romaji[self.current]

    def __init__(self):
        self.rand_list = []
        self.current = ""
        self.right_answer = ""

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
    q.create_list()
    while True:
        # print(q.current)
        await q.create_list()
        await config.channel.send("how do you say " + q.current +"?")
        await asyncio.sleep(config.time)


@client.event
async def on_ready():
    config._init(json.load(open("config.json", encoding="utf8")))
    #channel = client.guilds[0].channels[1]
    client.loop.create_task(bgtask())

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith(config.prefix):
        await Command.run(message.content[1:])
    else:
        print("answer received!")
        await q.verify(message.content, message.author)
        await q.reset(message.author)
        await data.save()
                       
@client.event
async def on_member_join(member):
    await config.channel.send("A new challenger apporaches")
    users.append(User(member))

print("initializing bot")
client.run(os.environ['TOKEN'])
