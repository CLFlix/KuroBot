from utils import *

from twitchio.ext import commands
from dotenv import load_dotenv

import os
import random

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHANNEL = os.getenv("CHANNEL")

POINTS_FILE = r'points.json'

class TwitchBot(commands.Bot):
    def __init__(self, rq_message):
        super().__init__(
            token=TOKEN,
            prefix="?",
            initial_channels=[CHANNEL]
        )
        self.rq_message = rq_message
        self.points = get_points_data(POINTS_FILE)
        # manage cooldowns
        self.last_point_time = {}

    ## helper methods
    def add_points(self, user, amount):
        if user not in self.points:
            self.points[user] = amount 
        else:
            self.points[user] += amount

    # add points as result to rps game
    def add_rps_points(self, user, rps_result):
        match rps_result:
            case "win":
                self.add_points(user, 3)
            case "tie":
                self.add_points(user, 1)

    ## events
    # print in console when bot is logged in and ready to be used
    async def event_ready(self):
        print(f"Logged in as {self.nick}")

    # give people points for chatting
    async def event_message(self, message):
        # message.author can be None when the bot is checking it's own messages
        if not message.author or message.author.name in ["nightbot", "streamelements"]:
            return
        
        # prevent points on command invoke
        if message.content.startswith("?") or message.content.startswith("!"):
            await self.handle_commands(message)
            return
        
        import time
        now = time.time()
        cooldown = 5

        user = message.author.name
        added_points = round(len(message.content) / 4)

        # prevent spamming
        if user not in self.last_point_time or (now - self.last_point_time[user]) >= cooldown:
            self.add_points(user, added_points)
            self.last_point_time[user] = now

        # this line is necessary to keep recognizing commands
        await self.handle_commands(message)

    ## useful commands
    @commands.command(name="test")
    async def test(self, ctx):
        await ctx.send("I'm responding! :D")

    # show all commands, don't show commands in hidden
    @commands.command(name="commands")
    async def cmds(self, ctx):
        hidden = ["commands", "test", "lb"]
        command_list = ", ".join(command for command in self.commands.keys() if command not in hidden)
        await ctx.send(f"@{ctx.author.name} Available commands: {command_list}")

    # display points
    @commands.command(name="points")
    async def points(self, ctx):
        name = ctx.author.name
        if name in self.points:
            if self.points[name] == 1:
                await ctx.send(f"@{name} You currently have 1 point.")
            else:
                await ctx.send(f"@{name} You currently have {self.points[name]} points.")
        else:
            await ctx.send(f"@{name} You currently have 0 points.")

    @commands.command(name="leaderboard")
    async def leaderboard(self, ctx):
        ranking = sorted(self.points.items(), key=lambda user: user[1], reverse=True)

        try:
            first, second, third = (
                f"{ranking[0][0]}: {ranking[0][1]}",
                f"{ranking[1][0]}: {ranking[1][1]}",
                f"{ranking[2][0]}: {ranking[2][1]}"
                )
            await ctx.send(f"@{ctx.author.name} {first}, {second}, {third}")

        except IndexError:
            if ctx.author.name in self.points:
                await ctx.send(f"@{ctx.author.name} There are less than 3 people in the ranking. You have {self.points[ctx.author.name]} points.")
            else:
                await ctx.send(f"@{ctx.author.name} There are less than 3 people in the ranking.")

    # leaderboard alias
    @commands.command(name="lb")
    async def lb(self, ctx):
        await self.leaderboard(ctx)

    # show now playing
    @commands.command(name="np")
    async def np(self, ctx):
        try:
            map_info = get_map()
            
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
            map_info = get_map()
            
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
        data = get_profile()
        global_rank, country_rank = data["pp_rank"], data["pp_country_rank"]

        await ctx.send(f"@{ctx.author.name} Global Rank: #{global_rank}, Country Rank: #{country_rank}")

    # show amount of playtime in hours
    @commands.command(name="playtime")
    async def playtime(self, ctx):
        data = get_profile()
        total_playtime = int(data["total_seconds_played"]) // 3600

        await ctx.send(f"@{ctx.author.name} _Kurookami_ has played osu! for a total of {total_playtime} hours.")

    # show playcount
    @commands.command(name="playcount")
    async def playcount(self, ctx):
        data = get_profile()
        playcount = data["playcount"]

        await ctx.send(f"@{ctx.author.name} _Kurookami_ has played osu! {playcount} times.")

    # show the chat if you want to accept requests or not (check main)
    @commands.command(name="rq")
    async def rq(self, ctx):
        await ctx.send(self.rq_message)

    ## Fun commands
    # roll a random number between 1 and a specified amount, with 100 as a default
    @commands.command(name="roll")
    async def roll(self, ctx, amount=100):
        random_number = random.randint(1, int(amount))
        await ctx.send(f"@{ctx.author.name} You rolled {random_number}")
    
    # replaces all r/l to w and sends it back in chat
    @commands.command(name="owo")
    async def owo(self, ctx, *, message: str = "Type in a message after '?owo' and I will owo-fy it."):
        owofied_message = message.replace("l", "w").replace("r", "w")
        await ctx.send(f"@{ctx.author.name} {owofied_message}")

    # return your message in SpOnGeBoB cApItAlIzAtIoN
    @commands.command(name="mock")
    async def mock(self, ctx, *, message: str = ""):
        if not message:
            await ctx.send(f"@{ctx.author.name} Enter a message and I will mock you ;)")
            return
        
        result = ""
        for i, letter in enumerate(message):
            if i % 2 == 0:
                result += letter.upper()
            else:
                result += letter.lower()
        
        await ctx.send(f"@{ctx.author.name} {result}")

    # rock paper scissors against bot
    @commands.command(name="rps")
    async def rps(self, ctx, choice):
        options = ["rock", "paper", "scissors"]

        player_choice = choice.lower()
        rps = random.choice(options)

        if player_choice not in options:
            await ctx.send(f"@{ctx.author.name} please choose rock, paper or scissors.")
            return
        
        outcomes = {
            ("rock", "rock"): "tie",
            ("rock", "paper"): "lose",
            ("rock", "scissors"): "win",
            ("paper", "rock"): "win",
            ("paper", "paper"): "tie",
            ("paper", "scissors"): "lose",
            ("scissors", "rock"): "lose",
            ("scissors", "paper"): "win",
            ("scissors", "scissors"): "tie",
        }

        result = outcomes[(player_choice, rps)]

        base_reply = f"You chose {player_choice}. I chose {rps}. "
        messages = {
            "win": "You win! 🎉",
            "lose": "You lose! 😢",
            "tie": "It's a tie. 🤝"
        }

        await ctx.send(f"@{ctx.author.name} {base_reply}{messages[result]}")

        if result in ("win", "tie"):
            self.add_rps_points(ctx.author.name, result)


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
        write_points_data(bot.points, POINTS_FILE)
        input("Press Enter to close...")

main()
