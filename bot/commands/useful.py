import random

from twitchio.ext import commands
from utils.utils import write_log, calculate_followage_days

class UsefulCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    def _log(self, e):
        from bot import LOG_FILE
        write_log(LOG_FILE, e)

    ## useful commands
    @commands.command(name="ping")
    async def ping(self, ctx):
        if ctx.author.name != self.bot.nick:
            return
        await ctx.send("Pong!")
    ping.category = "useful"
    ping.description = "This command can be used right before streaming to check " \
    "if the bot is working and responding."

    @commands.command(name="poll")
    async def poll(self, ctx, *, message):
        user = ctx.author.name
        mods_list = self.bot.read_mods()

        if user not in mods_list:
            await ctx.send(f"@{user} You do not have permission to use this command!")
            return
        
        if not self.bot.affiliate:
            await ctx.send(f"@{user} This channel is not Affiliate / Partner!")
            return
        
        title = message[:message.find("?") + 1]
        choices_list = message[message.find("?") + 1:].split(" ")
        choices = choices_list[1:]
        duration = 120

        created_poll = self.bot.create_poll(title, choices, duration)

        if not created_poll:
            await ctx.send(f"@{user} Couldn't create poll, details in log.")
            return
    poll.category = "useful"
    poll.description = "Using this command with the necessary parameters will " \
    "create a poll of 2 minutes. (moderator only)"

    # show all commands, don't show commands in hidden
    @commands.command(name="commands")
    async def cmds(self, ctx):
        await ctx.send(f"@{ctx.author.name} https://clflix.github.io/KuroBot/commands")
    cmds.category = "useful"
    cmds.description = "Show the link to this website in chat!"

    # classic lurk command with additional info about muting
    @commands.command(name="lurk")
    async def lurk(self, ctx):
        message = random.choice([
            "Thanks for the lurk! If you want to mute the audio, please mute the tab instead of the stream, otherwise you won't count as a viewer ;)",
            "is lurking! Appreciate you for stopping by! <3",
            "is watching you from a dark alley...",
            "does some other things while you're yapping in his ears. Thanks for dropping in! HeyGuys",
            "has your stream on in the background out of pity. TwitchLit"
        ])
        await ctx.send(
            f"@{ctx.author.name} {message}")
    lurk.category = "useful"
    lurk.description = "Let the streamer know you're there, but in the background 🧐"

# display socials in chat
    @commands.command(name="socials")
    async def socials(self, ctx):
        await ctx.send(f"@{ctx.author.name} {self.links}")
    socials.category = "useful"
    socials.description = "Display links to other social channels in the chat! These can be: YouTube, TikTok, Discord, Instagram, Twitter / X, or when the streamer prefers this, the link to their Linktree."

    @commands.command(name="youtube")
    async def youtube(self, ctx):
        link = self.bot.get_single_social("YouTube")
        if link:
            await ctx.send(f"@{ctx.author.name} {link}")
    youtube.category = "useful"
    youtube.description = "If the streamer has their YouTube linked in the bot, this command will give you this link. " \
    "Alias: !yt"
    youtube.aliases = ["yt"]

    @commands.command(name="discord")
    async def discord(self, ctx):
        link = self.bot.get_single_social("Discord")
        if link:
            await ctx.send(f"@{ctx.author.name} {link}")
    discord.category = "useful"
    discord.description = "If the streamer has their Discord server linked in the bot, this command will give you this link."

    @commands.command(name="tiktok")
    async def tiktok(self, ctx):
        link = self.bot.get_single_social("TikTok")
        if link:
            await ctx.send(f"@{ctx.author.name} {link}")
    tiktok.category = "useful"
    tiktok.description = "If the streamer has their TikTok linked in the bot, this command will give you this link."

    @commands.command(name="instagram")
    async def instagram(self, ctx):
        link = self.bot.get_single_social("Instagram")
        if link:
            await ctx.send(f"@{ctx.author.name} {link}")
    instagram.category = "useful"
    instagram.description = "If the streamer has their Instagram linked in the bot, this command will give you this link. " \
    "Alias: !insta"
    instagram.aliases = ["insta"]

    @commands.command(name="twitter")
    async def twitter(self, ctx):
        link = self.bot.get_single_social("Twitter / X")
        if link:
            await ctx.send(f"@{ctx.author.name} {link}")
    twitter.category = "useful"
    twitter.description = "If the streamer has their Twitter / X linked in the bot, this command will give you this link."

    @commands.command(name="linktree")
    async def linktree(self, ctx):
        link = self.bot.get_single_social("Linktree")
        if link:
            await ctx.send(f"@{ctx.author.name} {link}")
    linktree.category = "useful"
    linktree.description = "If the streamer has a Linktree or anything that has a similar goal linked in the bot, this command will show you the link."

    # shoutout the user specified
    @commands.command(name="shoutout", aliases=["so"])
    async def shoutout(self, ctx, user: str=None):
        invoker = ctx.author.name

        if not user or not user.encode("ascii", "ignore").decode():
            await ctx.send(f"@{invoker} You didn't specify a user to shoutout :/")
            return
        
        mods_list = self.bot.read_mods()
        if invoker not in mods_list:
            await ctx.send(f"@{invoker} You are not allowed to use this command!")
            return

        user = user.lower() if "@" not in user else user[1:].lower()
        link = f"https://www.twitch.tv/{user}"
        await ctx.send(f"Shoutout to {user} ! {link}")
    shoutout.category = "useful"
    shoutout.description = "Use this command and tag someone right behind it like '!shoutout @user' to shout out this user's Twitch channel! (mods only) " \
    "Alias: !so"

    @commands.command(name="claim")
    async def claim(self, ctx):
        user = ctx.author.name

        if user in self.bot.bonus_claimed:
            await ctx.send(f"@{user} You already claimed your first time bonus!")
            return

        self.bot.bonus_claimed.append(user)
        self.bot.add_points(user, 500)

        message = random.choice([
            "You just claimed 500 points! Use !commands to find out what you can do CorgiDerp",
            "Your first time bonus of 500 points have been claimed. Find out what you can do with them with !commands.",
            "500 points have been claimed. !commands will tell you what's possible with them. CoolCat",
            "You're now 500 points richer! Let's see what to do with them with !commands 4Head",
            "claimed 500 points! GoldPLZ"
        ])

        await ctx.send(f"@{user} {message}")
    claim.category = "useful"
    claim.description = "After using this command, you will have claimed your " \
    "first 500 bot points. You can obtain more points by chatting in the Twitch chat."

    @commands.command(name="daily")
    async def daily(self, ctx):
        user = ctx.author.name
        if user == self.bot.nick:
            return

        if user in self.bot.daily_claimed:
            await ctx.send(f"@{user} You already claimed your daily bonus!")
            return

        self.bot.add_points(user, 50)
        self.bot.daily_claimed.add(user)

        messages = [
            f"@{user} You just claimed your daily 50 points bonus!",
            f"@{user} You claimed a daily bonus! 50 points to you!",
            f"A daily bonus of 50 points was just claimed by @{user} !"
        ]
        choice = random.choice(messages)
        await ctx.send(choice)
    daily.category = "useful"
    daily.description = "Viewers can chime in on your stream and claim a bonus " \
    "of 50 points when they invoke this command."

    # display points
    @commands.command(name="points")
    async def points(self, ctx, username: str=None):
        user = ctx.author.name

        if not username or not username.encode("ascii", "ignore").decode():
            if user == self.bot.nick.lower():
                await ctx.send(f"@{self.bot.nick} is the points master! Infinite points to them!")
                return
            username = user
        else:
            username = username.lstrip("@").lower() if "@" in username else username.lower()

        if username == self.bot.nick.lower():
            await ctx.send(f"@{username} is the points master! Infinite points to them!")
            return

        if username in self.bot.user_points.keys():
            amount = self.bot.user_points[username]
            if amount == 1:
                msg = f"@{user} You currently have 1 point." if username == user else f"@{user} {username} currently has 1 point."
                await ctx.send(msg)
            else:
                if username == user:
                    messages = [
                        f"@{user} You currently have {amount} points.",
                        f"@{user} You have {amount} points in your bank!",
                        f"{amount} points are currently in @{user} 's possession.",
                        f"@{user} , you have {amount} points!",
                        f"@{user} there are {amount} points in your wallet!"
                    ]
                else:
                    messages = [
                        f"@{user} {username} currently has {amount} points.",
                        f"@{user} {username} has {amount} points in your bank!",
                        f"@{user} {amount} points are currently in {username} 's possession.",
                        f"@{user} , {username} has {amount} points!",
                        f"@{user} , there are {amount} points in {username} 's wallet!"
                    ]
                await ctx.send(random.choice(messages))
        else:
            msg = f"@{user} You currently have 0 points." if username == user else f"@{user} {username} has 0 points."
            await ctx.send(msg)
    points.category = "useful"
    points.description = "This command will show you how many bot points you have in this Twitch channel. " \
    "You can also check other people's wallet by throwing in their username behind it!"

    @commands.command(name="leaderboard", aliases=["lb"])
    async def leaderboard(self, ctx):
        ranking = sorted(self.bot.user_points.items(), key=lambda user: user[1], reverse=True)

        if not ranking:
            await ctx.send(f"@{ctx.author.name} No one is on the leaderboard yet!")
            return

        ranking.pop(0) # inf points is always index 0 because of sorting
        top_n = 3
        top_users = [f"{user}: {points}" for user, points in ranking[:top_n]]
        await ctx.send(f"@{ctx.author.name} " + ", ".join(top_users))
    leaderboard.category = "useful"
    leaderboard.description = "'!leaderboard' will show you the top 3 " \
    "bot point earners of this channel. Alias: !lb"

    # Get user's followage
    @commands.command(name="followage")
    async def followage(self, ctx, username=None):
        if username:
            user = username[1:] if "@" in username else username
            followage_message = f"@{ctx.author.name} @{user} has been following {self.bot.nick} for ..."
        else:
            user = ctx.author.name
            followage_message = f"@{user} You have been following {self.bot.nick} for ..."

        if self.bot.nick == user.lower():
            await ctx.send(f"@{user} You can't follow yourself, dummy")
            return

        if not await self.bot.user_exists(user):
            await ctx.send(f"@{ctx.author.name} This user doesn't exist.")
            return

        user_id = self.bot.get_user_id(user)

        try:
            followed_at = self.get_follower_data(user_id)
            if not followed_at:
                await ctx.send(f"@{ctx.author.name} This user doesn't follow {self.bot.nick}")
                return
        except ValueError as e:
            self._log(e)
            return
        
        followage = calculate_followage_days(followed_at)

        await ctx.send(followage_message.replace("...", followage))
    followage.category = "useful"
    followage.description = "By using this command, you can see how long you've been " \
    "following the streamer for! You can also tag someone like '!followage @user' " \
    "which will then show how long this user has been following the streamer for."

