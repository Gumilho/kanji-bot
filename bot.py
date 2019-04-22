import discord
import asyncio
import os

client = discord.Client()

async def bgtask():
	counter = 0
	channel = client.get_guild(493580129025654785).get_channel(493580129025654787)
	while True:
        	counter += 1
        	await channel.send(counter)
        	await asyncio.sleep(60)

@client.event
async def on_ready():
	print("ready!")
	client.loop.create_task(bgtask())
	await client.change_presence(activity=discord.Game(name="Weeb"))

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	else:
		await message.channel.send("Hi")

client.run(str(os.environ.get('TOKEN')))