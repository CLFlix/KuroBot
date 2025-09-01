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
    def __init__(self, rq_message):
        super().__init__(
            token=TOKEN,
            prefix="?",
            initial_channels=[CHANNEL]
        )
        self.rq_message = rq_message

    # print in console when bot is logged in and ready to be used
    async def event_ready(self):
        print(f"Logged in as {self.nick}")

    # When osuAuth and osuUsername are filled in in the .env file, this method can look up your osu! profile
    def get_profile(self):
        profile_url = "https://osu.ppy.sh/api/get_user"
        params = {"k": API_KEY, "u": osuUsername}
        response = requests.get(url=profile_url, params=params)

        data = response.json()[0]
        return data

    # When you have StreamCompanion running, the command !np and !nppp will request the map through this method
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
    
    # Quick testing
    @commands.command(name="test")
    async def test(self, ctx):
        await ctx.send("I'm responding! :D")

    # show all commands
    @commands.command(name="commands")
    async def cmds(self, ctx):
        await ctx.send(f"@{ctx.author.name} ?np, ?nppp, ?rank, ?playtime, ?playcount, ?rq")

    # show now playing
    @commands.command(name="np")
    async def np(self, ctx):
        try:
            map_info = self.get_map()
            
            mapid = map_info["mapid"]
            artist = map_info["artistRoman"] 
            title = map_info["titleRoman"]
            diffname = map_info["diffName"]
            mods = map_info["mods"]

            # Do nothing if there's only 1 mod
            if mods == "NM":
                mods = None
            elif len(mods) > 2:
                mods = mods.replace(",", "")

            if not mods:
                await ctx.send(f"@{ctx.author.name} Now playing: {artist} - {title} [{diffname}] https://osu.ppy.sh/b/{mapid}")
            else:
                await ctx.send(f"@{ctx.author.name} Now playing: {artist} - {title} [{diffname}] +{mods} https://osu.ppy.sh/b/{mapid}")
                
        except ConnectionError as e:
            await ctx.send(f"@{ctx.author.name} {e}")

    # show now playing with pp values for SS, 99% and 95%
    @commands.command(name="nppp") 
    async def nppp(self, ctx):
        try:
            map_info = self.get_map()
            
            mapid = map_info["mapid"]
            artist = map_info["artistRoman"]
            title = map_info["titleRoman"] 
            diffname = map_info["diffName"]
            
            pp_str = f"95%: {map_info['osu_95PP']:.0f}, 99%: {map_info['osu_99PP']:.0f}, 100%: {map_info['osu_SSPP']:.0f}"
            
            await ctx.send(f"@{ctx.author.name} Now playing: {artist} - {title} [{diffname}] https://osu.ppy.sh/b/{mapid} | PP: {pp_str}")
        except ConnectionError as e:
            await ctx.send(f"@{ctx.author.name} {e}")

    # show current rank (global and country)
    @commands.command(name="rank")
    async def rank(self, ctx):
        data = self.get_profile()
        global_rank, country_rank = data["pp_rank"], data["pp_country_rank"]

        await ctx.send(f"@{ctx.author.name} Global Rank: #{global_rank}, Country Rank: #{country_rank}")

    # show amount of playtime in hours
    @commands.command(name="playtime")
    async def playtime(self, ctx):
        data = self.get_profile()
        total_playtime = int(data["total_seconds_played"]) // 3600

        await ctx.send(f"@{ctx.author.name} _Kurookami_ has played osu! for a total of {total_playtime} hours.")

    # show playcount
    @commands.command(name="playcount")
    async def playcount(self, ctx):
        data = self.get_profile()
        playcount = data["playcount"]

        await ctx.send(f"@{ctx.author.name} _Kurookami_ has played osu! {playcount} times.")

    # show the chat if you want to accept requests or not (check main)
    @commands.command(name="rq")
    async def rq(self, ctx):
        await ctx.send(self.rq_message)


def main():
    ask_for_requests = True
    while ask_for_requests:
        requests_or_not = input("Do you accept map requests this stream? (y/n)\n")

        if requests_or_not.lower() == "y":
            message = "You're free to request any map you'd like to see me play. Just paste the link in the chat!"
            ask_for_requests = False
        elif requests_or_not.lower() == "n":
            message = "I will not be accepting map requests this stream :/. Maybe next stream ;)"
            ask_for_requests = False
        else:
            print("Not a valid answer. Please enter 'y' or 'n'.")

    bot = TwitchBot(message)
    try:
        bot.run()
    except Exception as e:
        print(f"Bot crashed: {e}")
    finally:
        input("Press Enter to close...")

main()
