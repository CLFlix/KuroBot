import random
import os

from bot.bot import LOG_FILE
from twitchio.ext import commands
from bot.utils.utils import get_map, get_profile, format_mods, write_log

osuUsername = os.getenv("osuUsername")

class OsuCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="np")
    async def np(self, ctx):
        try:
            map_info = get_map()
            
            mapid = map_info["mapid"]
            artist = map_info["artistRoman"] 
            title = map_info["titleRoman"]
            diffname = map_info["diffName"]
            mods = map_info["mods"]

            formatted_mods = format_mods(mods)

            if formatted_mods:
                await ctx.send(f"@{ctx.author.name} Now playing: {artist} - {title} [{diffname}] +{formatted_mods} https://osu.ppy.sh/b/{mapid}")
            else:
                await ctx.send(f"@{ctx.author.name} Now playing: {artist} - {title} [{diffname}] https://osu.ppy.sh/b/{mapid}")
                
        except ConnectionError as e:
            await ctx.send(f"@{self.bot.nick} , @{ctx.author.name} Something went wrong")
            write_log(LOG_FILE, f"[ERROR] - Couldn't get current playing map. StreamCompanion is most likely not running: {e}")
    np.category = "osu"
    np.description = "This will display the map that the streamer is currently playing."

    # show now playing with pp values for SS, 99% and 95%
    @commands.command(name="nppp") 
    async def nppp(self, ctx):
        try:
            map_info = get_map()
            mapid = map_info["mapid"]
            artist = map_info["artistRoman"]
            title = map_info["titleRoman"] 
            diffname = map_info["diffName"]
            mods = map_info["mods"]
            pp_str = f"95%: {map_info['osu_m95PP']:.0f}, 99%: {map_info['osu_m99PP']:.0f}, 100%: {map_info['osu_mSSPP']:.0f}"
            diff_settings = {
                "ar": map_info["mAR"],
                "od": map_info["mOD"],
                "hp": map_info["mHP"],
                "cs": map_info["mCS"]
            }

            formatted_mods = format_mods(mods)

            base = f"@{ctx.author.name} Now playing: {artist} - {title} [{diffname}]"
            link = f"https://osu.ppy.sh/b/{mapid}"
            diff = f"AR: {diff_settings["ar"]}, OD: {diff_settings['od']}, CS: {diff_settings['cs']}, HP: {diff_settings['hp']}"

            if formatted_mods:
                await ctx.send(f"{base} +{formatted_mods} {link} | {pp_str} | {diff}")
            else:
                await ctx.send(f"{base} {link} | {pp_str} | {diff}")

        except ConnectionError as e:
            await ctx.send(f"@{self.bot.nick} , @{ctx.author.name} Something went wrong")
            write_log(LOG_FILE, f"[ERROR] - Couldn't get current playing map. StreamCompanion is most likely not running: {e}")
    nppp.category = "osu"
    nppp.description = "This will make the bot reply with the map the streamer " \
    "is currently playing, along with the pp values for SS, 99% and 95%."

    # show current rank (global and country)
    @commands.command(name="rank")
    async def rank(self, ctx, *, user=osuUsername):
        try:
            found, data = get_profile(user)

            if not found:
                await ctx.send(f"@{ctx.author.name} {data}")
                return
            
            global_rank, country_rank = data["pp_rank"], data["pp_country_rank"]
            await ctx.send(f"@{ctx.author.name} Global Rank: #{global_rank}, Country Rank: #{country_rank}")

        except ConnectionError as e:
            await ctx.send(f"@{self.bot.nick} , @{ctx.author.name} Something went wrong")
            write_log(LOG_FILE, f"[ERROR] - Couldn't get {user}'s rank: {e}")
    rank.category = "osu"
    rank.description = "!rank will show the streamer's rank in chat! You can also provide a username and " \
    "the bot will search for that user's rank: !rank _Kurookami_"

    # show amount of playtime in hours
    @commands.command(name="playtime")
    async def playtime(self, ctx, *, user=osuUsername):
        try:
            found, data = get_profile(user)

            if not found:
                await ctx.send(f"@{ctx.author.name} {data}")
                return

            total_playtime = int(data["total_seconds_played"]) // 3600
            await ctx.send(f"@{ctx.author.name} {user} has played osu! for a total of {total_playtime} hours.")
        except ConnectionError as e:
            await ctx.send(f"@{self.bot.nick} , @{ctx.author.name} Something went wrong")
            write_log(LOG_FILE, f"[ERROR] - Couldn't get {user}'s playtime: {e}")
    playtime.category = "osu"
    playtime.description = "Calling this command will show how much time the streamer " \
    "has wasted in this game. Adding a username will find that information for that user: !playtime _Kurookami_"

    # show playcount
    @commands.command(name="playcount")
    async def playcount(self, ctx, *, user=osuUsername):
        try:
            found, data = get_profile(user)

            if not found:
                await ctx.send(f"@{ctx.author.name} {data}")
                return

            playcount = data["playcount"]
            await ctx.send(f"@{ctx.author.name} {user} has played osu! {playcount} times.")

        except ConnectionError as e:
            await ctx.send(f"@{self.bot.nick} , @{ctx.author.name} Something went wrong")
            write_log(LOG_FILE, f"[ERROR] - Couldn't get {user}'s playcount: {e}")
    playcount.category = "osu"
    playcount.description = "This command will show the streamer's playcount! " \
    "You can also find other users' playcount with !playcount _Kurookami_"

    # get general stats at once
    @commands.command(name="osustats")
    async def osustats(self, ctx, *, user=osuUsername):
        try:
            found, data = get_profile(user)

            if not found:
                await ctx.send(f"@{ctx.author.name} {data}")
                return

            global_rank, country_rank, pp, total_playtime, playcount = (
                data["pp_rank"],
                data["pp_country_rank"],
                data["pp_raw"],
                int(data["total_seconds_played"]) // 3600,
                data["playcount"]
            )

            formatted_message = f"{user}: #{global_rank}, Country rank: #{country_rank} - pp: {pp} - Playtime: {total_playtime}h - Playcount: {playcount}"
            await ctx.send(f"@{ctx.author.name} {formatted_message}")
            
        except ConnectionError as e:
            await ctx.send(f"@{self.bot.nick} @{ctx.author.name} Something went wrong getting osu! profile.")
            write_log(LOG_FILE, f"[ERROR] - Couldn't get {user}'s osustats: {e}")
    osustats.category = "osu"
    osustats.description = "This command is basically rank, playtime and playcount combined. " \
    "You can also call this for another user: !osustats _Kurookami_"

    @commands.command(name="profile")
    async def profile(self, ctx, *, user=osuUsername):
        try:
            found, data = get_profile(user)

            if not found:
                await ctx.send(f"@{ctx.author.name} {data}")
                return
            
            user_id = data["user_id"]
            await ctx.send(f"@{ctx.author.name} https://osu.ppy.sh/users/{user_id}")
        except ConnectionError as e:
            await ctx.send(f"@{self.bot.nick} @{ctx.author.name} Something went wrong getting osu! profile.")
            write_log(LOG_FILE, f"[ERROR] - Couldn't find {user}'s profile: {e}")
    profile.category = "osu"
    profile.description = "Show the link to the osu! profile of the streamer! " \
    "You can also get someone else's profile: !profile _Kurookami_"

    # show the chat if you want to accept requests or not (self.rq_message comes from main())
    @commands.command(name="rq")
    async def rq(self, ctx):
        if self.bot.map_requests:
            message = random.choice([
                "You're free to request any map you'd like to see me play. Just paste the link in the chat! CorgiDerp",
                "If you wanna see me play a specific map, just put the link of it in chat ArgieB8",
                "Want to see a particular map? Just yeet the link in the chat FBCatch",
                "You have a banger map in mind? Tell me! GoatEmotey",
                "Specific circles you want to see? Just paste the link in here and we'll see how I do..."
            ])
        else:
            message = random.choice([
                "I will not be accepting map requests this stream BabyRage Maybe next stream..",
                "map requests will be skipped right now. BigSad",
                "denied.. FBBlock Maybe next time I will accept map requests.",
                "Not taking map requests at the moment. TearGlove Sorry!",
                "Map requests are closed for now. BOP Maybe another time!"
            ])
        await ctx.send(f"@{ctx.author.name} {message}")
    rq.category = "osu"
    rq.description = "The streamer can decide whether they want to receive " \
    "beatmap requests. This command will then show whether they accept those requests or not."

    # change streaming category to osu!
    @commands.command(name="category")
    async def category(self, ctx):
        user = ctx.author.id
        mods_list = self.bot.read_mods()

        if user not in mods_list:
            return await ctx.send("You are not allowed to use this command!")

        await ctx.send("Changing stream category to osu!")
        self.bot.update_stream_category()
    category.category = "osu"
    category.description = "Change the streaming category to osu! (mods / streamer only)"