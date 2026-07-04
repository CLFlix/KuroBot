from twitchio.ext import commands

import random

class FunCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # roll a random number between 1 and a specified amount, with 100 as a default
    @commands.command(name="roll")
    async def roll(self, ctx, amount=100):
        if amount > 1000000000000:
            amount = 100
        random_number = random.randint(1, int(amount))
        await ctx.send(f"@{ctx.author.name} You rolled {random_number}")
    roll.category = "fun"
    roll.description = "If you don't specify the maximum, this command will " \
    "roll a random number between 1 and 100. By specifying the maximum like " \
    "'roll 1000', this will roll any number between 1 and the specified number, " \
    "in this case 1000."

    # replaces all r/l to w and sends it back in chat
    @commands.command(name="owo")
    async def owo(self, ctx, *, message: str = "Type in a message after '!owo' and I will owo-fy it."):
        owofied_message = message.translate(str.maketrans({"r": "w", "l": "w", "R": "W", "L": "W"}))
        owofied_message = owofied_message.replace("TH", "F").replace("th", "f").replace("Th", "F")
        await ctx.send(f"@{ctx.author.name} {owofied_message}")
    owo.category = "fun"
    owo.description = "This command will return your message after " \
    "replacing all the l's and r's with w's, and replacing all 'th' with 'f'. This way, 'Hello world' " \
    "becomes 'Hewwo wowwd'."

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
    mock.category = "fun"
    mock.description = "Hanging in the same style as 'owo', this command " \
    "will return your message in SpOnGeBoB cApItAlIzAtIoN."

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
            self.bot.add_rps_points(ctx.author.name, result)
    rps.category = "fun"
    rps.description = "Play rock, paper, scissors with the bot! If you win, " \
    "you get 15 points. If you tie with the bot, you gain 5 points."

    @commands.command(name="rob", aliases=["steal"])
    async def rob(self, ctx, username: str=None):
        invoker = ctx.author.name

        if not username or not username.encode("ascii", "ignore").decode():
            await ctx.send(f"@{invoker} You didn't specify who you want to rob points from!")
            return
        
        username = username.lstrip("@").lower() if "@" in username else username.lower()

        if username in self.bot.robbed:
            await ctx.send(f"@{invoker} {username} already has been robbed today!")
            return

        if self.bot.nick.lower() == invoker:
            await ctx.send(f"@{invoker} A bit unfair to steal from your viewers, hm? YouWHY")
            return
        elif self.bot.nick.lower() == username:
            await ctx.send(f"@{invoker} You can't steal from the points master... LUL")
            return
        elif username == invoker:
            await ctx.send(f"@{invoker} what are you doing?? Stealing from yourself? LUL")
            return

        if username not in self.bot.user_points.keys():
            await ctx.send(f"@{invoker} This user doesn't have any points, or just doesn't exist lol")
            return
        
        if invoker in self.bot.robbers.keys() and len(self.bot.robbers[invoker]) == 3:
            await ctx.send(f"@{invoker} You've already tried robbing 3 times!")
            return

        if invoker in self.bot.robbers.keys():
            self.bot.robbers[invoker].append(username)
        else:
            self.bot.robbers[invoker] = [username]


        steal_chance = 0.33

        if random.random() > steal_chance:
            fine = round(self.bot.user_points[invoker] * random.uniform(0.02, 0.04))
            self.bot.remove_points(invoker, fine)
            lost_points_message = f"You just lost 1 point!" if fine == 1 else f"You just lost {fine} points!"
            messages = [
                f"@{invoker} You failed to rob {username}... {lost_points_message}",
                f"{username} managed to escape {invoker} 's rob! {lost_points_message}",
                f"@{invoker} {username} kept all of their points safely secured. {lost_points_message}",
                f"{username} held on to his points @{invoker} {lost_points_message}!",
                f"All of {username} 's points were kept away from {invoker} this time! {lost_points_message}"
            ]
            await ctx.send(random.choice(messages))
            return
        
        percentage = random.uniform(0.03, 0.07)
        robbed_points = round(self.bot.user_points[username] * percentage)
        self.bot.remove_points(username, robbed_points)
        self.bot.add_points(invoker, robbed_points)
        self.bot.robbed.add(username)

        messages = [
            f"@{invoker} You stole {robbed_points} points from {username} .",
            f"{username} lost {robbed_points} points because of {invoker} !",
            f"{robbed_points} were stolen from {username} by {invoker} .",
            f"Oh no! {invoker} robbed {username} of {robbed_points} points!",
            f"{username} didn't secure their vault enough.. {invoker} stole {robbed_points} points."
        ]
        await ctx.send(random.choice(messages))
    rob.category = "fun"
    rob.description = "Steal a small portion of points from another chatter! Watch out, though, " \
    "there's only a 1/3 chance you will successfully steal. If you don't, you lose points... " \
    "Example: !rob KurookamiTV " \
    "Alias: !steal"

    # remember to drink!
    @commands.command(name="hydrate")
    async def hydrate(self, ctx):
        if self.bot.affiliate:
            return
        
        messages = [
            "Hydration check! You gotta take a sip!",
            "H2O.exe initializing...",
            "Chat demands a sip of your drink!",
            "Achievement unlocked: Remembered to Hydrate",
            "Take a sip. Your body will thank you.",
        ]

        await ctx.send(f"@{self.nick} {random.choice(messages)}")
    hydrate.category = "fun"
    hydrate.description = "Remind the streamer to drink water! Only enabled when the streamer " \
    "says they're not an Affiliate / Partner."

    @commands.command(name="posture")
    async def posture(self, ctx):
        if self.bot.affiliate:
            return
        
        messages = [
            "Posture check!",
            "Check your posture!",
            "Still sitting straight?",
            "You're not breaking your back, are you?",
            "Gamer posture detected... Correct it!",
            "Attention! Entering pro posture mode...",
        ]

        await ctx.send(f"@{self.nick} {random.choice(messages)}")
    posture.category = "fun"
    posture.description = "Make the streamer check their posture. Only enabled when the streamer " \
    "says they're not an Affiliate / Partner."

    @commands.command(name="stretch")
    async def stretch(self, ctx):
        if self.bot.affiliate:
            return
        
        messages = [
            "Streeeeeeeetch!",
            "Time to stretch for a sec!",
            "Help your blood flow, stretch!",
            "Get off that chair for a little!",
            "Stand up and stretch a bit!",
            "How long ago did you stretch?"
        ]

        await ctx.send(f"@{self.nick} {random.choice(messages)}")
    stretch.category = "fun"
    stretch.description = "Get the streamer to stretch for a second. Only enabled when the streamer " \
    "says they're not an Affiliate / Partner."