import asyncio
import json
SCORE = []
KANJI = {}
GUILD_ID = 0
CHANNEL_ID = 0
TIME = 0
CONFIG = {}
# KANJI_SIZE = 0
cur = ""
async def load():
        print("loading data... ", end="")
        data = json.load(open("data.json","r"))
        config = json.load(open("config.json","r"))
        SCORE = data["score"].copy()
        KANJI = data["kanji"].copy()
        #print(list(KANJI))
        GUILD_ID = config["guild"]
        # print(GUILD_ID)
        CHANNEL_ID = config["channel"]
        TIME = config["time"]
        # KANJI_SIZE = len(KANJI)
        print("done")
