from twitchio.ext import commands
import os
from dotenv import load_dotenv 

load_dotenv()

BOT_NICK = os.getenv("BOT_NICK")
TOKEN = os.getenv("TOKEN")
CHANNEL = os.getenv("CHANNEL")

class TwitchBot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=TOKEN,
            prefix="!",
            initial_channels=[CHANNEL]
        )

    async def event_ready(self):
        print(f"Logged in as {self.nick}")

    @commands.command(name="hello")
    async def hello(self, ctx):
        await ctx.send(f"Hi there @{ctx.author.name}!")

bot = TwitchBot()
bot.run()