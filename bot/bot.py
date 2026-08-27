from bot.utils.utils import *
from bot.utils.eventsub_listener import eventsub_listener
from bot.utils.twitch_api import TwitchAPI

from twitchio.ext import commands
from packaging import version

from dotenv import load_dotenv

import os
import time
from datetime import datetime as dt
import asyncio
import webbrowser
from pydantic import BaseModel
import sys

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import threading

load_dotenv()

CURRENT_VERSION = "v4.0.0"

TOKEN = os.getenv("TOKEN")
BROADCASTER_ID = int(os.getenv("BROADCASTER_ID"))
CHANNEL = os.getenv("CHANNEL")
CLIENT_ID = os.getenv("CLIENT_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
osuUsername = os.getenv("osuUsername")

POINTS_FILE = r'points.json'
FIRST_TIME_BONUS_FILE = r'first_time_bonus_claimed.txt'
SOCIALS_FILE = r'socials.json'

date_format = "%Y-%m-%d_%H-%M-%S"
LOG_FILE = f'logs/{dt.now().strftime(date_format)}.txt'

shutdown_event = asyncio.Event()

class KuroBot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=TOKEN,
            prefix="!",
            initial_channels=[CHANNEL]
        )

        # let first_time_startup run first, otherwise log file will
        # become undefined, trying to look in a directory that doesn't exist
        first_time_startup()
        write_log(LOG_FILE, "\n\t".join([
            "\n\tTHIS IS A KUROBOT LOG FILE",
            "If you have a problem or an error that was not caused by you,",
            "please provide this file when reporting the error.",
            "Bug Reporting: https://github.com/CLFlix/KuroBot/issues",
            "Suggestions: https://github.com/CLFlix/KuroBot/discussions/categories/suggestions\n\n"
        ]))

        if getattr(sys, 'frozen', False):
            sys.stderr = open(LOG_FILE, 'a', buffering=1, encoding='utf-8')

        self.api = TwitchAPI(ACCESS_TOKEN, LOG_FILE)

        self.initialized = False
        self.map_requests = False
        self.affiliate = False
        self.update_title = False
        self.update_available = False

        self.launch_backend()
        webbrowser.open("http://localhost:7273/initializeBot")

        self.user_points = get_points_data(POINTS_FILE)
        self.bonus_claimed = get_bonus_claimed(FIRST_TIME_BONUS_FILE)
        self.daily_claimed = set()
        self.links = read_socials_links(SOCIALS_FILE)
        if self.links != "No socials added":
            self.links_dict = dict(item.split(": ", 1) for item in self.links.split(", "))

        # manage chat message points cooldowns
        self.last_point_time = {}

        # manage 5 gambles per stream
        self.gamble_cooldown = {}

        # manage 3 robs per stream
        self.robbers = {}
        # only get robbed once per stream
        self.robbed = set()

        # initialize self.endwith_redeemed for check
        self.endwith_redeemed = False

        self._load_cogs()

    def _load_cogs(self):
        from bot.commands.useful import UsefulCommands
        from bot.commands.osu import OsuCommands
        from bot.commands.fun import FunCommands
        from bot.commands.redeem import RedeemCommands

        self.add_cog(UsefulCommands(self))
        self.add_cog(OsuCommands(self))
        self.add_cog(FunCommands(self))
        self.add_cog(RedeemCommands(self))

    async def run_forever(self):
        start_task = asyncio.create_task(self.start())
        try:
            await shutdown_event.wait()
        finally:
            await self.stop()
            await start_task

    def check_for_update(self):
        url = f"https://api.github.com/repos/CLFlix/KuroBot/releases/latest"
        response = requests.get(url, timeout=10)

        if not response:
            return

        data = response.json()
        latest_version = data["tag_name"].lstrip("v")

        if version.parse(latest_version) > version.parse(CURRENT_VERSION):
            self.update_available = {
                "update": True,
                "latest": latest_version,
                "release_url": data["html_url"]
            }
            return

        self.update_available = {
            "update": False,
            "latest": CURRENT_VERSION,
            "release_url": None
        }

    def launch_backend(self):
        self.bot_state = {
            "rank": None,
            "current_title": None,
        }
        
        app = FastAPI()

        BASE_DIR = Path(__file__).resolve().parent.parent
        STATIC_DIR = BASE_DIR / "website" / "out"

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )

        app.mount("/KuroBot", StaticFiles(directory=STATIC_DIR, html=True), name="static")

        @app.get("/")
        def dashboard():
            return FileResponse(STATIC_DIR / "dashboard.html")

        @app.get("/initializeBot")
        def initializeBot():
            return FileResponse(STATIC_DIR / "initializeBot.html")
            
        class InitializeData(BaseModel):
            rq: bool
            affiliate: bool
            update: bool

        @app.post("/initialize")
        def initialize(data: InitializeData):
            self.map_requests = data.rq
            self.affiliate = data.affiliate
            self.update_title = data.update
            self.initialized = True
            return

        @app.get("/isRunning")
        def is_running():
            return "hello"

        @app.get("/initStatus")
        def initStatus():
            return self.initialized
        
        @app.get("/updateStatus")
        def is_update_available():
            return self.update_available
        
        @app.get("/takeRequests")
        def take_requests():
            return self.map_requests

        @app.get("/titleUpdaterOn")
        def titleUpdaterOn():
            return self.update_title
        
        @app.get("/listener")
        def listenerOn():
            return self.affiliate

        @app.get("/twitchTitle")
        def twitchTitle():
            self.bot_state["current_title"] = self.get_stream_title()
            return self.bot_state["current_title"]
        
        @app.get("/rank")
        def rank():
            profile = get_profile(osuUsername)[1]
            self.bot_state["rank"] = profile["pp_rank"]
            return f"#{self.bot_state["rank"]}"
        
        @app.get("/points")
        def get_points():
            return self.get_top_5_points()

        @app.get("/update_title")
        async def fire_updater():
            await self.title_updater()

        @app.post("/toggleRequests")
        def toggleRequests():
            self.map_requests = not self.map_requests
            write_log(LOG_FILE, f"[NOTICE] - [OPTIONS] Toggled Requests to {"ON" if self.map_requests else "OFF"}")

        @app.post("/stop")
        async def stop_bot():
            shutdown_event.set()

        def start_api():
            import uvicorn
            uvicorn.run(app, host="127.0.0.1", port=7273, log_config=None) # log_level='critical' for dev

        threading.Thread(target=start_api, daemon=True).start()

    async def stop(self):
        write_log(LOG_FILE, "[INFO] - Stopping bot..")
        write_bonus_claimed(self.bonus_claimed, FIRST_TIME_BONUS_FILE)
        write_log(LOG_FILE, f"[INFO] - First time bonus data saved")

        expired_vips = check_expired_vips()
        for expired_vip in expired_vips:
            self.api.remove_vip(expired_vip)

        self.clear_banned_users()
        del self.user_points[self.user_id]
        write_points_data(self.user_points, POINTS_FILE)
        write_log(LOG_FILE, f"[INFO] - Points data saved")

        write_log(LOG_FILE, "[INFO] - Stopped bot. Bye!")
        await self.close()

    ## export commands
    def export_commands(self):
        order = ["commands", "followage", "lurk", "socials", "youtube", "discord", "tiktok", "twitter",
                 "instagram", "linktree", "shoutout", "points", "claim", "daily", "leaderboard", "poll",
                 "category", "ping", "rq", "np", "nppp", "profile", "rank", "playcount", "playtime",
                 "osustats", "hydrate", "posture", "stretch", "owo", "mock", "rps", "roll", "rob",
                 "shush", "endwith", "invert", "zoom", "memecam", "gift", "gamble", "double", "vip"]

        written = set()
        with open(r'website/public/static/commands.txt', 'w', encoding='utf-8') as commands_file:
            for cmd_name in order:
                if cmd_name in self.commands:
                    cmd = self.commands[cmd_name]
                    description = getattr(cmd, "description", "/")
                    category = getattr(cmd, "category", "/")
                    commands_file.write(f"{cmd_name} - {description} - {category}\n")
                    written.add(cmd_name)
        print("Commands succesfully exported to 'website/public/static/commands.txt'")

    ## helper methods
    def add_points(self, user_id, username, amount):
        if int(user_id) == self.user_id:
            write_log(LOG_FILE, f"[INFO] - Skipping add_points, user is self.nick")
            return
        if user_id not in self.user_points:
            self.user_points[user_id] = amount 
        else:
            self.user_points[user_id] = round(self.user_points[user_id] + amount)
        write_log(LOG_FILE, f"[INFO] - Added {amount} to {username}'s points: {self.user_points[user_id]}")

    # add points as result to rps game
    def add_rps_points(self, user_id, username, rps_result):
        match rps_result:
            case "win":
                self.add_points(user_id, username, 15)
            case "tie":
                self.add_points(user_id, username, 5)

    # check points for points redeeming
    def remove_points(self, user_id, username, item_cost):
        if int(user_id) == self.user_id:
            return True, f"Infinite points - {item_cost}?? lol"

        if user_id in self.user_points:
            if self.user_points[user_id] < item_cost:
                write_log(LOG_FILE, f"[INFO] - {username} does not have enough for an item that costs {item_cost}: {self.user_points[user_id]}")
                return False, f"@{username} You don't have enough points! You need {item_cost - self.user_points[user_id]} more points!"
            else:
                self.user_points[user_id] = round(self.user_points[user_id] - item_cost)
                write_log(LOG_FILE, f"[INFO] - Subtracted {item_cost} points from {username}: {self.user_points[user_id]}")
                return True, f"This costed @{username} {item_cost} points."
        else:
            write_log(LOG_FILE, f"[INFO] - {username} does not have enough for an item that costs {item_cost}: {self.user_points[user_id]}")
            return False, f"@{username} You don't have enough points! You need {item_cost} more points!"

    def get_top_5_points(self):
        ranking = sorted(self.user_points.items(), key=lambda user: user[1], reverse=True)
        ranking.pop(0) # inf points is always index 0 because of sorting

        top_n = 5
        top_5 = {user_id: points for user_id, points in ranking[:top_n]}

        ranking_with_usernames = {}
        for user_id, points in top_5.items():
            user_name = self.get_user_name(user_id)
            ranking_with_usernames[user_name] = points
        
        return ranking_with_usernames

## events
    async def event_ready(self):
        self.user_points[self.user_id] = float("inf")
        self.check_for_update()
        self.get_mods_list()
        # self.export_commands() # ONLY USED FOR UPDATING WEBSITE COMMANDS

        while not self.initialized:
            await asyncio.sleep(0.5)
        if self.map_requests:
            write_log(LOG_FILE, "[NOTICE] - [OPTIONS] Bot started with requests ON")
        else:
            write_log(LOG_FILE, "[NOTICE] - [OPTIONS] Bot started with requests OFF")

        if self.affiliate:
            self.loop.create_task(eventsub_listener(self.handle_redemptions))
            write_log(LOG_FILE, "[NOTICE] - [OPTIONS] Affiliate / Partner enabled. Locked commands: !hydrate, !stretch, !posture. Redemptions Listener ON")
        else:
            write_log(LOG_FILE, "[NOTICE] - [OPTIONS] Affiliate / Partner disabled. Unlocked commands: !hydrate, !stretch, !posture. Redemptions Listener OFF")

        if self.update_title:
            self.loop.create_task(self.title_updater_loop())
            write_log(LOG_FILE, "[NOTICE] - [OPTIONS] Automatic Title Updater ON")
        else:
            write_log(LOG_FILE, "[NOTICE] - [OPTIONS] Automatic Title Updater OFF")

    # give people points for chatting
    async def event_message(self, message):
        # message.author can be None when the bot is checking it's own messages
        if not message.author or message.author.name in ["nightbot", "streamelements", "ronniabot"]:
            return

        if message.author.name == self.nick:
            await self.handle_commands(message)
            return

        # prevent points on command invoke
        if message.content.startswith("?") or message.content.startswith("!"):
            await self.handle_commands(message)
            return
        
        now = time.time()
        cooldown = 5

        user_id = message.author.id
        added_points = min(15, round(len(message.content) / 4))

        # prevent spamming
        if user_id not in self.last_point_time or (now - self.last_point_time[user_id]) >= cooldown:
            self.add_points(user_id, message.author.name, added_points)
            self.last_point_time[user_id] = now

        # this line is necessary to keep recognizing commands
        await self.handle_commands(message)

    # handle twitch points redemptions
    async def handle_redemptions(self, event):
        channel = self.get_channel(CHANNEL)
        if event == "revocation":
            channel.send("Please check the console and contact the bot dev with this issue.")

        redemption = event["reward"]["title"]
        if redemption.startswith("Exchange"):
            user_id = event["user_id"]
            user_name = event["user_login"].lower()
            cost = event["reward"]["cost"]

            self.add_points(user_id, user_name, cost)
            await channel.send(f"@{user_name} Your redemption has been acknowlged.")

    def get_single_social(self, social):
        try:
            return self.links_dict[social]
        except:
            write_log(LOG_FILE, f"[NOTICE] - No social set for: {social}")

    def clear_banned_users(self):
        banned_users = self.get_banned_users()

        for user_id in banned_users:
            if user_id in self.user_points.keys():
                del self.user_points[user_id]
        
    def read_mods(self):
        with open(r'mods_list.txt', 'r', encoding='utf-8') as mods_list:
            mods = mods_list.readlines()
        return mods

    def get_user_id(self, user):
        return self.api.get_user_id(user)

    def get_user_name(self, user_id):
        return self.api.get_user_name(user_id)
    
    def get_mods_list(self):
        return self.api.get_mods_list(self.user_id)

    def get_banned_users(self):
        return self.api.get_banned_users()

    def get_follower_data(self, user_id):
        return self.api.get_follower_data(user_id)

    def add_vip(self, user_id):
        return self.api.add_vip(user_id)

    def create_poll(self, title, choices, duration):
        return self.api.create_poll(title, choices, duration)

    def get_stream_title(self):
        return self.api.get_stream_title()

    def update_stream_title(self, new_stream_title):
        self.api.update_stream_title(new_stream_title)

    def update_stream_category(self):
        self.api.update_stream_category()

    # generalized function for title_updater_loop and post mapping
    async def title_updater(self):
        current_title = self.get_stream_title()
        self.bot_state["current_title"] = current_title
        profile = get_profile(osuUsername)[1]
        current_rank = profile["pp_rank"]

        try:
            new_stream_title = edit_stream_title(current_title, current_rank)
            if new_stream_title != current_title:
                self.update_stream_title(new_stream_title)

        except SyntaxError as e:
            write_log(LOG_FILE, f"[ERROR] - Caught SyntaxError while editing stream title: {e}")
            
        except ValueError as e:
            write_log(LOG_FILE, f"[NOTICE] - {e}")

        return

    # this loop will restart every 10 minutes, updating the stream title
    # with the current osu! rank, keeping the title up-to-date
    async def title_updater_loop(self):
        while not shutdown_event.is_set():
            await self.title_updater()

            try:
                await asyncio.wait_for(shutdown_event.wait(), timeout=600) # 10 minute cooldown before restarting loop
            except asyncio.TimeoutError:
                pass