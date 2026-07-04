import random

from bot.bot import LOG_FILE
from twitchio.ext import commands
from bot.utils.utils import write_log

class RedeemCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="shush")
    async def shush(self, ctx):
        user = ctx.author.name
        shush_cost = 2500
        can_afford, afford_message = self.bot.remove_points(user, shush_cost)

        if can_afford:
            await ctx.send(f"@{self.bot.nick} You can't speak for the next 5 minutes! {afford_message}")
            write_log(LOG_FILE, f"[INFO] - Shush has been claimed by {user}")
        else:
            await ctx.send(afford_message)
    shush.category = "redeem"
    shush.description = "Redeeming 2500 points, the streamer cannot speak for the next 5 minutes!"

    # streamer meme cam
    @commands.command(name="memecam")
    async def memecam(self, ctx):
        user = ctx.author.name
        memecam_cost = 500
        can_afford, afford_message = self.bot.remove_points(user, memecam_cost)

        if can_afford:
            await ctx.send(f"@{self.bot.nick} You have to throw a silly effect over your camera for the next 10 minutes! {afford_message}")
            write_log(LOG_FILE, f"[INFO] - Memecam has been claimed by {user}")
        else:
            await ctx.send(afford_message)
    memecam.category = "redeem"
    memecam.description = "Redeeming 500 of the user's points, " \
    "the streamer has to turn on an effect / filter over their camera " \
    "for the next 10 minutes."

    @commands.command(name="zoom")
    async def zoom(self, ctx):
        user = ctx.author.name
        zoom_cost = 500
        can_afford, afford_message = self.bot.remove_points(user, zoom_cost)

        if not can_afford:
            await ctx.send(afford_message)
            return
        
        await ctx.send(f"@{self.bot.nick} You now have to zoom in your camera for the next 10 minutes! {afford_message}")
        write_log(LOG_FILE, f"[INFO] - Zoom has been claimed by {user}")

    zoom.category = "redeem"
    zoom.description = "Make the streamer zoom in their camera for 10 minutes for 500 points!"

    @commands.command(name="invert")
    async def invert(self, ctx):
        user = ctx.author.name
        invert_cost = 250
        can_afford, afford_message = self.bot.remove_points(user, invert_cost)

        if not can_afford:
            await ctx.send(afford_message)
            return

        await ctx.send(f"@{self.bot.nick} Turn your camera upside-down for the next 10 minutes! {afford_message}")
        write_log(LOG_FILE, f"[INFO] - Invert has been claimed by {user}")
    invert.category = "redeem"
    invert.description = "For 250 points, you can make the streamer turn their camera upside-down for 10 minutes."

    # end stream with this map
    @commands.command(name="endwith")
    async def endwith(self, ctx, map_link=None):
        user = ctx.author.name
        endwith_cost = 300

        if self.bot.endwith_redeemed:
            await ctx.send(f"@{user} Endwith already has been redeemed!")
            return

        if map_link == None:
            await ctx.send(f"@{user} Please send the map link or the title of the song you'd like to see the stream end with: '!endwith <link or title>'")
            return
            
        can_afford, afford_message = self.bot.remove_points(user, endwith_cost)

        if can_afford:
            self.bot.endwith_redeemed = True
            await ctx.send(f"@{self.bot.nick} You have to end stream with {map_link}! {afford_message}")
            write_log(LOG_FILE, f"[INFO] - Endwith has been claimed by {user}")
        else:
            await ctx.send(afford_message)
    endwith.category = "redeem"
    endwith.description = "Redeeming 300 of the user's points, " \
    "the streamer has to end the stream or current osu! session " \
    "with the specified map."

    @commands.command(name="gift")
    async def gift(self, ctx, *, message: str):
        gifter = ctx.author.name
        parts = message.split()

        if len(parts) != 2:
            await ctx.send(f"@{gifter} Make sure you send the command in this format: '!gift @<user> <amount>'")
            return

        receiver = parts[0].lstrip("@").lower()

        try:
            amount = int(parts[1])
        except ValueError:
            await ctx.send(f"@{gifter} Make sure you send the command in this format: '!gift @<user> <amount>'")
            return

        if amount <= 0:
            await ctx.send(f"@{gifter} You must gift a positive amount of points!")
            return

        if receiver.lower() == gifter:
            await ctx.send(f"@{gifter} You cant gift points to yourself!")
            return

        if not await self.bot.user_exists(receiver):
            await ctx.send(f"@{gifter} That user doesn't exist on Twitch!")
            return

        can_afford, afford_message = self.bot.remove_points(gifter, amount)

        if not can_afford:
            await ctx.send(afford_message)
            return

        return_message = random.choice([
            f"How generous! @{gifter} gifted {amount} points to @{receiver} !",
            f"Look at that! {amount} points have been gifted by @{gifter} to @{receiver}. ",
            f"@{gifter} send {amount} points to @{receiver} 's side! W",
            f"@{receiver} is now {amount} points richer because of @{gifter} !",
            f"@{gifter} could miss {amount} points and gave it to @{receiver} !"
        ])
        await ctx.send(return_message)
        self.bot.add_points(receiver, amount)
        write_log(LOG_FILE, f"[INFO] - {gifter} gifted {amount} points to {receiver}")
    gift.category = "redeem"
    gift.description = "You can gift points to another user, if you " \
    "have enough points to do so. '!gift @KurookamiTV 500' will subtract " \
    "500 points from the invoker, and add 500 points to KurookamiTV's total."

    @commands.command(name="gamble")
    async def gamble(self, ctx, amount=None):
        user = ctx.author.name

        if not amount:
            amount = 0

        try:
            amount = int(amount)
        except Exception:
            await ctx.send(f"@{user} Enter the number you want to gamble (text like '3k' won't be accepted)")
            return

        if user in self.bot.gamble_cooldown.keys() and self.bot.gamble_cooldown[user] == 5:
            await ctx.send(f"@{user} You can only use gamble 5 times per stream.")
            return

        if amount < 0:
            await ctx.send(f"@{user} You tried gambling with a negative value? Take this: https://youtu.be/dQw4w9WgXcQ?si=l32ZYljZ4vhSA5hC")
            return

        if amount == 0:
            await ctx.send(f"@{user} You didn't specify an amount. Usage: '!gamble <amount>'")
            return

        if amount > self.bot.user_points[user]:
            await ctx.send(f"@{user} You cannot afford this gamble!")
            return

        if user in self.bot.gamble_cooldown.keys():
            self.bot.gamble_cooldown[user] += 1
        else:
            self.bot.gamble_cooldown[user] = 1

        self.bot.remove_points(user, amount)

        won = random.choice([0,1])
        if won:
            dice = random.choice([1, 2, 3, 4, 5, 6]) # roll a dice 1-6
            dice_mapping = {1: 1, 2: 1.1, 3: 1.2, 4: 1.3, 5: 1.4, 6: 1.5} # multiplier mapping
            multiplier = dice_mapping.get(dice)
            
            match round(multiplier - 1, 1):
                case 0:
                    self.bot.add_points(user, amount)
                    await ctx.send(f"@{user} You didn't win, you didn't lose.. You got your {amount} points back.")
                    write_log(LOG_FILE, f"[INFO] - {user} gambled {amount} points and broke even.")
                case _:
                    won_points = round(amount * multiplier) if amount * multiplier != 0 else 1
                    await ctx.send(f"@{user} Congrats, you won {won_points} point{"" if won_points == 1 else "s"}!")
                    self.bot.add_points(user, won_points)
                    write_log(LOG_FILE, f"[INFO] - {user} won {won_points} points by gambling {amount} points")
        else:
            await ctx.send(f"@{user} Sadge, you lost {amount} points...")
            write_log(LOG_FILE, f"[INFO] - {user} lost {amount} points by gambling.")
    gamble.category = "redeem"
    gamble.description = "Gamble your points away! You have a 1 in 2 chance of winning. If you do, " \
    "a 6-sided dice will roll and decide on a multiplier which will calculate how much you win. This can " \
    "only be used 5 times per stream (per bot run)."

    @commands.command(name="double", aliases=["dorn"])
    async def double(self, ctx):
        user = ctx.author.name
        if user not in self.bot.user_points or self.bot.user_points[user] == 0:
            await ctx.send(f"@{user} you don't have any points.")

        won = random.choice([0,1])
        if won:
            self.bot.add_points(user, self.bot.user_points[user])
            await ctx.send(f"@{user} You won! You now have double your original amount of points!")
            write_log(LOG_FILE, f"[INFO] - {user} won the double or nothing: {self.bot.user_points[user]}")
        else:
            self.bot.user_points = 0
            await ctx.send(f"@{user} You lost... You're back at 0 points...")
            write_log(LOG_FILE, f"[INFO] - {user} lost the double or nothing.")
    double.category = "redeem"
    double.description = "Double or nothing! When using this command, you go all in. " \
    "You either lose everything, or end up with double the amount you had originally!"

    # temporary VIP status
    @commands.command(name="vip")
    async def vip(self, ctx):
        vip_cost = 1000000
        user = ctx.author.name

        can_afford, afford_message = self.bot.remove_points(user, vip_cost)
        
        if not can_afford:
            await ctx.send(afford_message)
            return

        user_id = self.bot.get_user_id(user)
        succes, status_code = self.bot.add_vip(user_id) # try adding VIP

        if succes:
            message = random.choice([
                f"A VIP slot has been claimed by @{user} ! {afford_message}",
                f"A new VIP spot has been taken by @{user} ! bleedPurple",
                f"@{user} You are now a VIP! {afford_message} CurseLit",
                f"R.I.P. to @{user} 's 1 million points, but they're now a VIP! 🎉",
                f"One less VIP slot available because @{user} just spent 1 million points on one! Congrats!"
            ])
            await ctx.send(message)
        else:
            self.bot.add_points(user, vip_cost)
            match status_code:
                case 422:
                    await ctx.send(f"@{user} You already are a VIP!")
                    write_log(LOG_FILE, f"[WARN] - {user} tried claiming VIP while already being one.")
                case _:
                    await ctx.send(f"@{self.bot.nick} Something went wrong. @{user} No points were deducted.")
                    write_log(LOG_FILE, f"[ERROR] - Couldn't add VIP to {user}: Status Code {status_code}")
    vip.category = "redeem"
    vip.description = "Redeeming 1.000.000 points, you can " \
    "claim VIP status on the streamer's Twitch channel! " \
    "The bot will reply with a message saying this is temporary, " \
    "but the streamer can, of course, decide theirselves whether " \
    "this is permanent or not."