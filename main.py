from utils import *
from token_refreshers.refresh_vip_token import refresh_tokens
from token_refreshers.refresh_polls_access_token import refresh_token_polls
from eventsub_listener import eventsub_listener

from twitchio.ext import commands
from dotenv import load_dotenv

import os
import random

load_dotenv()

TOKEN = os.getenv("TOKEN")
BROADCASTER_ID = os.getenv("BROADCASTER_ID")
CHANNEL = os.getenv("CHANNEL")
CLIENT_ID = os.getenv("CLIENT_ID")

ACCESS_TOKEN_VIP = os.getenv("ACCESS_TOKEN_VIP")
ACCESS_TOKEN_POLLS = os.getenv("ACCESS_TOKEN_POLLS")

osuUsername = os.getenv("osuUsername")

POINTS_FILE = r'points.json'
FIRST_TIME_BONUS_FILE = r'first_time_bonus_claimed.txt'
LOG_FILE = r'log.txt'

class TwitchBot(commands.Bot):
    def __init__(self, rq_message, affiliate):
        super().__init__(
            token=TOKEN,
            prefix="?",
            initial_channels=[CHANNEL]
        )

        self.rq_message = rq_message
        self.affiliate = affiliate

        self.points = get_points_data(POINTS_FILE)
        self.bonus_claimed = get_bonus_claimed(FIRST_TIME_BONUS_FILE)

        # manage chat message points cooldowns
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

    # check points for points redeeming
    def remove_points(self, user, item_cost):
        if user in self.points:
            if self.points[user] < item_cost:
                return False, f"@{user} You don't have enough points! You need {item_cost - self.points[user]} more points!"
            else:
                self.points[user] -= item_cost
                return True, f"This costed @{user} {item_cost} points."
        else:
            return False, f"@{user} You don't have enough points! You need {item_cost} more points!"

    # handle twitch points redemptions
    async def handle_redemptions(self, event):
        channel = self.get_channel(CHANNEL)
        if event == "revocation":
            channel.send("Please check the console and contact the bot dev with this issue.")
        
        redemption = event["reward"]["title"]
        if redemption.startswith("Exchange"):
            user = event["user_name"].lower()
            cost = event["reward"]["cost"]

            self.add_points(user, cost)

            await channel.send(f"@{user} Your redemption has been acknowlged.")

    # check if a user exists
    async def user_exists(self, username) -> bool:
        global ACCESS_TOKEN_VIP

        url = f"https://api.twitch.tv/helix/users?login={username}"
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN_VIP}",
            "Client-Id": CLIENT_ID
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 401:
            try:
                ACCESS_TOKEN_VIP = refresh_tokens()
                print("Refreshed bot tokens")
            except Exception as e:
                log_error(LOG_FILE, e)
                print("Something went wrong refreshing VIP access token, used to check if a user exists.")
                return False
            
            headers["Authorization"] = f"Bearer {ACCESS_TOKEN_VIP}"
            requests.get(url, headers=headers)

            if response.status_code not in (200, 203):
                print(f"Failed to check user: {response.text}")
                return False

        data = response.json()
        return len(data["data"]) > 0

    # add VIP status to user
    def add_vip(self, user_id):
        url = "https://api.twitch.tv/helix/channels/vips"
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN_VIP}",
            "Client-Id": CLIENT_ID
        }
        params = {
            "broadcaster_id": BROADCASTER_ID,
            "user_id": user_id
        }

        try:
            response = requests.post(url, headers=headers, params=params)
        except ConnectionError:
            return "Something went wrong assigning VIP status.."

        if response.status_code == 204:
            return True, 204
        elif response.status_code == 422: # user already is VIP
            return False, 422
        else:
            log_error(LOG_FILE, response.text)
            return False, response.status_code
    
    def create_poll(self, title, choices, duration):
        uri = "https://api.twitch.tv/helix/polls"
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN_POLLS}",
            "Client-Id": CLIENT_ID,
            "Content-Type": "application/json"
        }

        body = {
            "broadcaster_id": BROADCASTER_ID,
            "title": title,
            "choices": [{"title": choice} for choice in choices],
            "duration": duration,
            "channel_points_voting_enabled": False
        }

        response = requests.post(uri, headers=headers, json=body)

        if response.status_code == 401:
            try:
                new_polls_token = refresh_token_polls()
                print("Refreshed poll token")
            except Exception as e:
                print(f"Refresh failed: {e}")
                return
            
            headers["Authorization"] = f"Bearer {new_polls_token}"
            response = requests.post(uri, headers=headers, json=body)

            if response.status_code not in (200, 202):
                log_error(LOG_FILE, response.text)
                raise ConnectionError("Error creating poll.")
            
            return True
        
        elif response.status_code == 200:
            return True
        else:
            log_error(LOG_FILE, response.text)
            return False


    ## events
    # print in console when bot is logged in and ready to be used
    async def event_ready(self):
        print(f"Logged in as {self.nick}")
        if self.affiliate:
            self.loop.create_task(eventsub_listener(self.handle_redemptions))

    # give people points for chatting
    async def event_message(self, message):
        # message.author can be None when the bot is checking it's own messages
        if not message.author or message.author.name in ["nightbot", "streamelements", "ronniabot"]:
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
    
    @commands.command(name="poll")
    async def poll(self, ctx, *, message):
        user = ctx.author.name

        with open(r'mods_list.txt', 'r', encoding='utf-8') as mods_list:
            mods = mods_list.readlines()

        mods = [user.strip() for user in mods]
        if user not in mods:
            await ctx.send(f"@{user} You do not have permission to use this command!")
            return
        
        title = message[:message.find("?") + 1]
        choices_list = message[message.find("?") + 1:].split(" ")
        choices = choices_list[1:]
        duration = 120

        created_poll = self.create_poll(title, choices, duration)

        if created_poll:
            return
        else:
            await ctx.send(f"@{user} Couldn't create poll, check the log file.")
            return

    # show all commands, don't show commands in hidden
    @commands.command(name="commands")
    async def cmds(self, ctx):
        hidden = ["commands", "test", "lb", "claim", "poll"]
        command_list = ", ".join(command for command in self.commands.keys() if command not in hidden)
        await ctx.send(f"@{ctx.author.name} Available commands: {command_list}")

    @commands.command(name="claim")
    async def claim(self, ctx):
        user = ctx.author.name

        if user in self.bonus_claimed:
            await ctx.send(f"@{user} You already claimed your first time bonus!")
            return

        self.bonus_claimed.append(user)
        self.add_points(user, 500)
        await ctx.send(f"@{user} You just claimed 500 points! Use ?commands to find out what you can do ;)")

    # display points
    @commands.command(name="points")
    async def points(self, ctx):
        user = ctx.author.name
        if user in self.points:
            if self.points[user] == 1:
                await ctx.send(f"@{user} You currently have 1 point.")
            else:
                await ctx.send(f"@{user} You currently have {self.points[user]} points.")
        else:
            await ctx.send(f"@{user} You currently have 0 points.")

    @commands.command(name="leaderboard")
    async def leaderboard(self, ctx):
        ranking = sorted(self.points.items(), key=lambda user: user[1], reverse=True)

        if not ranking:
            await ctx.send(f"@{ctx.author.name} No one is on the leaderboard yet!")
            return

        top_n = 3
        top_users = [f"{user}: {points}" for user, points in ranking[:top_n]]
        await ctx.send(f"@{ctx.author.name} " + ", ".join(top_users))

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

            formatted_mods = format_mods(mods)

            if formatted_mods:
                await ctx.send(f"@{ctx.author.name} Now playing: {artist} - {title} [{diffname}] +{formatted_mods} https://osu.ppy.sh/b/{mapid}")
            else:
                await ctx.send(f"@{ctx.author.name} Now playing: {artist} - {title} [{diffname}] https://osu.ppy.sh/b/{mapid}")
                
        except ConnectionError as e:
            await ctx.send(f"@{self.nick}, @{ctx.author.name} Something went wrong")
            log_error(LOG_FILE, e)

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
            
            formatted_mods = format_mods(mods)

            if formatted_mods:
                pp_str = f"95%: {map_info['osu_m95PP']:.0f}, 99%: {map_info['osu_m99PP']:.0f}, 100%: {map_info['osu_mSSPP']:.0f}"
                await ctx.send(f"@{ctx.author.name} Now playing: {artist} - {title} [{diffname}] +{formatted_mods} https://osu.ppy.sh/b/{mapid} | PP: {pp_str}")
            else:
                pp_str = f"95%: {map_info['osu_95PP']:.0f}, 99%: {map_info['osu_99PP']:.0f}, 100%: {map_info['osu_SSPP']:.0f}"
                await ctx.send(f"@{ctx.author.name} Now playing: {artist} - {title} [{diffname}] https://osu.ppy.sh/b/{mapid} | PP: {pp_str}")

        except ConnectionError as e:
            await ctx.send(f"@{self.nick}, @{ctx.author.name} Something went wrong")
            log_error(LOG_FILE, e)

    # show current rank (global and country)
    @commands.command(name="rank")
    async def rank(self, ctx):
        try:
            data = get_profile()
            global_rank, country_rank = data["pp_rank"], data["pp_country_rank"]

            await ctx.send(f"@{ctx.author.name} Global Rank: #{global_rank}, Country Rank: #{country_rank}")
        except ConnectionError as e:
            await ctx.send(f"@{self.nick}, @{ctx.author.name} Something went wrong")
            log_error(LOG_FILE, e)

    # show amount of playtime in hours
    @commands.command(name="playtime")
    async def playtime(self, ctx):
        try:
            data = get_profile()
            total_playtime = int(data["total_seconds_played"]) // 3600

            await ctx.send(f"@{ctx.author.name} {osuUsername} has played osu! for a total of {total_playtime} hours.")
        except ConnectionError as e:
            await ctx.send(f"@{self.nick}, @{ctx.author.name} Something went wrong")
            log_error(LOG_FILE, e)

    # show playcount
    @commands.command(name="playcount")
    async def playcount(self, ctx):
        try:
            data = get_profile()
            playcount = data["playcount"]

            await ctx.send(f"@{ctx.author.name} {osuUsername} has played osu! {playcount} times.")
        except ConnectionError as e:
            await ctx.send(f"@{self.nick}, @{ctx.author.name} Something went wrong")
            log_error(LOG_FILE, e)

    # show the chat if you want to accept requests or not (self.rq_message comes from main())
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
    async def rps(self, ctx, choice=None):
        options = ["rock", "paper", "scissors"]

        if not choice:
            await ctx.send(f"@{ctx.author.name} please choose rock, paper or scissors.")
            return
        
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

    ## redeem points
    # streamer meme cam
    @commands.command(name="memecam")
    async def memecam(self, ctx):
        user = ctx.author.name
        memecam_cost = 500

        can_afford, afford_message = self.remove_points(user, memecam_cost)

        if can_afford:
            await ctx.send(f"@{self.nick} You have to throw a silly effect over your camera for the next 10 minutes! {afford_message}")
        else:
            await ctx.send(afford_message)

    # end stream with this map
    @commands.command(name="endwith")
    async def endwith(self, ctx, map_link):
        user = ctx.author.name
        endwith_cost = 300

        can_afford, afford_message = self.remove_points(user, endwith_cost)

        if can_afford:
            await ctx.send(f"@{self.nick} You have to end stream with {map_link}! {afford_message}")
        else:
            await ctx.send(afford_message)

    @commands.command(name="gift")
    async def gift(self, ctx, *, message: str):
        gifter = ctx.author.name

        message = message.split()
        if len(message) != 2:
            await ctx.send(f"@{gifter} Make sure you send the command in this format: '?gift @<user> <amount>'")
            return

        # remove "@" from receiver + case consistency for points
        receiver = message[0][1:].lower()

        try:
            amount = int(message[1])
        except ValueError:
            await ctx.send(f"@{gifter} Make sure you send the command in this format: '?gift @<user> <amount>'")
            return

        if amount <= 0:
            await ctx.send(f"@{gifter} You must gift a positive amount of points!")
            return

        if receiver.lower() == gifter:
            await ctx.send(f"@{gifter} You cant gift points to yourself!")
            return

        user_exists: bool = await self.user_exists(receiver)

        if not user_exists:
            await ctx.send(f"@{gifter} That user doesn't exist on Twitch!")
            return

        can_afford, afford_message = self.remove_points(gifter, amount)

        if can_afford:
            await ctx.send(f"How generous! @{gifter} gifted {amount} points to @{receiver}!")
            self.add_points(receiver, amount)
            return
            
        await ctx.send(afford_message)

    # temporary VIP status
    @commands.command(name="vip")
    async def vip(self, ctx):
        global ACCESS_TOKEN_VIP

        vip_cost = 10000
        user = ctx.author.name

        can_afford, afford_message = self.remove_points(user, vip_cost)
        
        if not can_afford:
            await ctx.send(afford_message)
            return

        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN_VIP}",
            "Client-Id": CLIENT_ID
        }

        # initial try to get user id
        response = requests.get(
            "https://api.twitch.tv/helix/users",
            headers=headers,
            params={"login": user}
        )

        if response.status_code == 401: # Unauthorized: token expired
            try:
                ACCESS_TOKEN_VIP = refresh_tokens()
                print("Refreshed bot tokens")
            except Exception as e:
                await ctx.send(f"@{self.nick}, @{user} Token refresh failed. Try again later.")
                log_error(LOG_FILE, e)
                return
            
            # retry getting user id once
            headers['Authorization'] = f"Bearer {ACCESS_TOKEN_VIP}"
            response = requests.get(
                "https://api.twitch.tv/helix/users",
                headers=headers,
                params={"login": user}
            )

        user_data = response.json()

        if not user_data.get("data"):
            await ctx.send(f"Couldn't fetch user ID for @{user}.")
            return

        user_id = user_data["data"][0]["id"]
                        
        succes, status_code = self.add_vip(user_id) # try adding VIP

        if succes:
            await ctx.send(f"{self.nick} A temporary VIP status has been redeemed by @{user}! {afford_message}")
        else:
            self.points[user] += vip_cost
            match status_code:
                case 422:
                    await ctx.send(f"@{user} You already are a VIP!")
                case _:
                    await ctx.send(f"@{self.nick} Something went wrong. @{user} No points were deducted.")


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

    ask_for_affiliate = True
    while ask_for_affiliate:
        affiliate_or_not = input("Are you a Twitch Affiliate or Partner? (y/n)\n")

        if affiliate_or_not.lower() == "y":
            affiliate = True
            ask_for_affiliate = False
        elif affiliate_or_not.lower() == "n":
            affiliate = False
            ask_for_affiliate = False
        else:
            print("Not a valid answer. Please enter 'y' or 'n'.")

    bot = TwitchBot(message, affiliate)
    clean_logs(LOG_FILE)
    try:
        bot.run()
    except Exception as e:
        print(f"Bot crashed: {e}")
    finally:
        write_points_data(bot.points, POINTS_FILE)
        write_bonus_claimed(bot.bonus_claimed, FIRST_TIME_BONUS_FILE)
        input("Press Enter to close...")

main()
