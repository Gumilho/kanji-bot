import discord
import asyncio
import random
import os
import json
import config

client = discord.Client()

async def save():
        print("saving files...", end="")
        json.dump(SCORE,open("data.json","w"))
        print("done")

async def bgtask():
	# channel = client.get_guild(int(GUILD_ID)).get_channel(int(CHANNEL_ID))
        channel = client.guilds[0].channels[1]
        print("initializing background task")
        while True:
                print(list(config.KANJI))
                sel = random.choice(list(config.KANJI))
                await channel.send(sel)
                cur = KANJI[sel]
                print(cur)
                await asyncio.sleep(config.TIME)

@client.event
async def on_ready():
        await config.load()
        print(config.KANJI)
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
