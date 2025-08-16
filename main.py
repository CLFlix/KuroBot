from twitchio.ext import commands
import os
import requests
from dotenv import load_dotenv 

load_dotenv()

BOT_NICK = os.getenv("BOT_NICK")
TOKEN = os.getenv("TOKEN")
CHANNEL = os.getenv("CHANNEL")
osuUsername = os.getenv("osuUsername")
API_KEY = os.getenv("osuAuth")

class TwitchBot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=TOKEN,
            prefix="!",
            initial_channels=[CHANNEL]
        )

    async def event_ready(self):
        print(f"Logged in as {self.nick}")

    @commands.command(name="np")
    async def np(self, ctx):
        with open(r'C:\Program Files (x86)\StreamCompanion\Files\np_all.txt') as np_file:
            message = np_file.read()

        await ctx.send(f"@{ctx.author.name} Now playing: {message}")

    @commands.command(name="rank")
    async def rank(self, ctx):
        profile_url = "https://osu.ppy.sh/api/get_user"
        params = {"k": API_KEY, "u": osuUsername}

        response = requests.get(url=profile_url, params=params)
        data = response.json()[0]

        global_rank, country_rank = data["pp_rank"], data["pp_country_rank"]

        await ctx.send(f"@{ctx.author.name} Global Rank: #{global_rank}, Country Rank: #{country_rank}")

bot = TwitchBot()
bot.run()