from twitchio.ext import commands
import os
import requests
from dotenv import load_dotenv

load_dotenv()

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

    def get_profile(self):
        profile_url = "https://osu.ppy.sh/api/get_user"
        params = {"k": API_KEY, "u": osuUsername}
        response = requests.get(url=profile_url, params=params)

        data = response.json()[0]
        return data

    # Since this endpoint is only called occasionally through !np, the
    # performance impact of doing this instead of websockets should be irrelevant.
    def get_map(self):
        companion_url = "http://localhost:20727/json"

        try:
            response = requests.get(companion_url)
        except:
            raise ConnectionError("StreamCompanion is not running or not accessible")
        
        response.encoding = 'utf-8-sig'
        data = response.json()
        return data
    
    async def event_ready(self):
        print(f"Logged in as {self.nick}")

    @commands.command(name="cmds")
    async def cmds(self, ctx):
        await ctx.send(f"@{ctx.author.name} !np, !nppp, !rank, !playtime, !playcount")

    @commands.command(name="np")
    async def np(self, ctx):
        try:
            map_info = self.get_map()
            
            mapid = map_info["mapid"]
            artist = map_info["artistRoman"] 
            title = map_info["titleRoman"]
            diffname = map_info["diffName"]
            
            await ctx.send(f"@{ctx.author.name} Now playing: {artist} - {title} [{diffname}] https://osu.ppy.sh/b/{mapid}")
        except ConnectionError as e:
            await ctx.send(f"@{ctx.author.name} {e}")

    @commands.command(name="nppp") 
    async def nppp(self, ctx):
        try:
            map_info = self.get_map()
            
            mapid = map_info["mapid"]
            artist = map_info["artistRoman"]
            title = map_info["titleRoman"] 
            diffname = map_info["diffName"]
            
            pp_str = f"96%: {map_info['osu_96PP']:.0f}, 97%: {map_info['osu_97PP']:.0f}, 98%: {map_info['osu_98PP']:.0f}, 99%: {map_info['osu_99PP']:.0f}, 100%: {map_info['osu_SSPP']:.0f}"
            
            await ctx.send(f"@{ctx.author.name} Now playing: {artist} - {title} [{diffname}] https://osu.ppy.sh/b/{mapid} | PP: {pp_str}")
        except ConnectionError as e:
            await ctx.send(f"@{ctx.author.name} {e}")

    @commands.command(name="rank")
    async def rank(self, ctx):
        data = self.get_profile()
        global_rank, country_rank = data["pp_rank"], data["pp_country_rank"]

        await ctx.send(f"@{ctx.author.name} Global Rank: #{global_rank}, Country Rank: #{country_rank}")

    @commands.command(name="playtime")
    async def playtime(self, ctx):
        data = self.get_profile()
        total_playtime = int(data["total_seconds_played"]) // 3600

        await ctx.send(f"@{ctx.author.name} _Kurookami_ has played osu! for a total of {total_playtime} hours.")

    @commands.command(name="playcount")
    async def playcount(self, ctx):
        data = self.get_profile()
        playcount = data["playcount"]

        await ctx.send(f"@{ctx.author.name} _Kurookami_ has played osu! {playcount} times.")

bot = TwitchBot()
bot.run()