from utils import *
from refresh_access_token import refresh_access_token
from eventsub_listener import eventsub_listener

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

CURRENT_VERSION = "v2.3.0"

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

request_headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Client-Id": CLIENT_ID,
    "Content-Type": "application/json"
}

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

        if getattr(sys, 'frozen', False):
            sys.stderr = open(LOG_FILE, 'w')

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
        from commands.useful import UsefulCommands
        from commands.osu import OsuCommands
        from commands.fun import FunCommands
        from commands.redeem import RedeemCommands

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

        BASE_DIR = Path(__file__).resolve().parent
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
            req_points = {}
            for username, points_amount in self.user_points.items():
                if username != self.nick:
                    req_points[username] = points_amount
            return req_points

        @app.get("/update_title")
        async def fire_updater():
            await self.title_updater()

        @app.post("/toggleRequests")
        def toggleRequests():
            self.map_requests = not self.map_requests

        @app.post("/stop")
        async def stop_bot():
            shutdown_event.set()

        def start_api():
            import uvicorn
            uvicorn.run(app, host="127.0.0.1", port=7273, log_config=None) # log_level='critical' for dev

        threading.Thread(target=start_api, daemon=True).start()

    async def stop(self):
        write_bonus_claimed(self.bonus_claimed, FIRST_TIME_BONUS_FILE)
        write_log(LOG_FILE, f"First time bonus data saved")

        self.clear_banned_users()
        self.user_points[self.nick] = 0
        write_points_data(self.user_points, POINTS_FILE)
        write_log(LOG_FILE, f"Points data saved")

        write_log(LOG_FILE, "Bye! :D")
        await self.close()

    ## export commands
    def export_commands(self):
        order = ["commands", "followage", "lurk", "socials", "youtube", "discord", "tiktok", "twitter",
                 "instagram", "linktree", "shoutout", "points", "claim", "daily", "leaderboard", "poll",
                 "category", "ping", "rq", "np", "nppp", "profile", "rank", "playcount", "playtime",
                 "osustats", "hydrate", "posture", "stretch", "owo", "mock", "rps", "roll", "rob",
                 "shush", "endwith", "invert", "zoom", "memecam", "gift", "gamble", "vip"]

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
    def add_points(self, user, amount):
        if user not in self.user_points:
            self.user_points[user] = amount 
        else:
            self.user_points[user] = round(self.user_points[user] + amount)

    # add points as result to rps game
    def add_rps_points(self, user, rps_result):
        match rps_result:
            case "win":
                self.add_points(user, 15)
            case "tie":
                self.add_points(user, 5)

    # check points for points redeeming
    def remove_points(self, user, item_cost):
        if user == self.nick:
            return True, f"Infinite points - {item_cost}?? lol"

        if user in self.user_points:
            if self.user_points[user] < item_cost:
                return False, f"@{user} You don't have enough points! You need {item_cost - self.user_points[user]} more points!"
            else:
                self.user_points[user] = round(self.user_points[user] - item_cost)
                return True, f"This costed @{user} {item_cost} points."
        else:
            return False, f"@{user} You don't have enough points! You need {item_cost} more points!"

## events
    async def event_ready(self):
        self.user_points[self.nick] = float("inf")
        self.check_for_update()
        await self.get_mods_list()
        # self.export_commands() # ONLY USED FOR UPDATING WEBSITE COMMANDS

        while not self.initialized:
            await asyncio.sleep(0.5)

        if self.affiliate:
            self.loop.create_task(eventsub_listener(self.handle_redemptions))
        if self.update_title:
            self.loop.create_task(self.title_updater_loop())

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

        user = message.author.name
        added_points = min(15, round(len(message.content) / 4))

        # prevent spamming
        if user not in self.last_point_time or (now - self.last_point_time[user]) >= cooldown:
            self.add_points(user, added_points)
            self.last_point_time[user] = now

        # this line is necessary to keep recognizing commands
        await self.handle_commands(message)

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

    def get_single_social(self, social):
        try:
            return self.links_dict[social]
        except:
            pass

    async def get_mods_list(self):
        global ACCESS_TOKEN, request_headers

        uri = "https://api.twitch.tv/helix/moderation/moderators"
        params = {"broadcaster_id": BROADCASTER_ID}


        response = requests.get(uri, headers=request_headers, params=params)

        if response.status_code == 401:
            try:
                ACCESS_TOKEN = refresh_access_token()
                request_headers["Authorization"] = f"Bearer {ACCESS_TOKEN}"
            except Exception as e:
                write_log(LOG_FILE, e)

            response = requests.get(uri, headers=request_headers, params=params)

            if response.status_code != 200:
                write_log(LOG_FILE, response.text)
                raise ConnectionError(f"Error getting mods list. More detailed error in {LOG_FILE}")

        try:
            data = response.json()["data"]
            mods_list = [mod["user_login"] for mod in data]

            with open("mods_list.txt", 'w', encoding='utf-8') as mods_file:
                for mod in mods_list:
                    mods_file.write(f"{mod}\n")
                mods_file.write(self.nick)

        except requests.exceptions.JSONDecodeError:
            raise RuntimeError("Couldn't get moderators list.")
        
    def get_banned_users(self):
        global ACCESS_TOKEN, request_headers

        uri = "https://api.twitch.tv/helix/moderation/banned"
        params = {"broadcaster_id": BROADCASTER_ID}

        response = requests.get(uri, headers=request_headers, params=params)

        if response.status_code == 401:
            try:
                ACCESS_TOKEN = refresh_access_token()
                request_headers["Authorization"] = f"Bearer {ACCESS_TOKEN}"
            except Exception as e:
                write_log(LOG_FILE, e)

            response = requests.get(uri, headers=request_headers, params=params)

            if response.status_code != 200:
                write_log(LOG_FILE, response.text)
                raise ConnectionError("Couldn't get banned users list.")

        try:
            data: list = response.json()["data"]
            banned_users = set()
            for banned_user in data:
                banned_users.add(banned_user["user_login"])
            return banned_users
        except requests.exceptions.JSONDecodeError:
            write_log(LOG_FILE, "Couldn't decode banned users list response.")

    def clear_banned_users(self):
        banned_users = self.get_banned_users()

        for user in banned_users:
            if user in self.user_points.keys():
                del self.user_points[user]
        
    def read_mods(self):
        with open(r'mods_list.txt', 'r', encoding='utf-8') as mods_list:
            mods = mods_list.readlines()
        mods_list = [user.strip() for user in mods]
        return mods_list

    # check if a user exists
    async def user_exists(self, username) -> bool:
        global ACCESS_TOKEN, request_headers

        url = f"https://api.twitch.tv/helix/users?login={username}"

        response = requests.get(url, headers=request_headers)

        if response.status_code == 401:
            try:
                ACCESS_TOKEN = refresh_access_token()
            except Exception as e:
                write_log(LOG_FILE, e)
                return False
            
            request_headers["Authorization"] = f"Bearer {ACCESS_TOKEN}"
            response = requests.get(url, headers=request_headers)

            if not response.ok:
                write_log(LOG_FILE, response.text)
                return False

        data = response.json()
        return len(data["data"]) > 0

    def get_user_id(self, user):
        global ACCESS_TOKEN, request_headers

        url = "https://api.twitch.tv/helix/users"
        params = {
            "login": user
        }

        # initial try to get user id
        response = requests.get(url, headers=request_headers, params=params)

        if response.status_code == 401: # Unauthorized: token expired
            try:
                ACCESS_TOKEN = refresh_access_token()
                request_headers['Authorization'] = f"Bearer {ACCESS_TOKEN}"
            except ConnectionError as e:
                write_log(LOG_FILE, e)
                return
            
            # retry getting user id once
            response = requests.get(url, headers=request_headers, params=params)

        try:
            user_data = response.json()
            return user_data["data"][0]["id"]
        except requests.exceptions.JSONDecodeError as e:
            write_log(LOG_FILE, e)

    def get_follower_data(self, user_id):
        global ACCESS_TOKEN, request_headers

        url = "https://api.twitch.tv/helix/channels/followers"
        params = {
            "user_id": user_id,
            "broadcaster_id": BROADCASTER_ID
        }

        response = requests.get(url, headers=request_headers, params=params)

        if response.status_code == 401:
            try:
                ACCESS_TOKEN = refresh_access_token()
                request_headers["Authorization"] = f"Bearer {ACCESS_TOKEN}"
            except ConnectionError as e:
                write_log(LOG_FILE, e)
                return
            
            response = requests.get(url, headers=request_headers, params=params)

            if not response.ok:
                write_log(LOG_FILE, response.text)
                return
            
        try:
            data = response.json()["data"]
            if not data:
                return
            return data[0]["followed_at"]
        except requests.exceptions.JSONDecodeError as e:
            write_log(LOG_FILE, "Invalid or no response getting followage.")

    # add VIP status to user
    def add_vip(self, user_id):
        url = "https://api.twitch.tv/helix/channels/vips"
        params = {
            "broadcaster_id": BROADCASTER_ID,
            "user_id": user_id
        }

        try:
            response = requests.post(url, headers=request_headers, params=params)
        except ConnectionError:
            return "Something went wrong assigning VIP status.."

        if response.status_code == 204:
            return True, 204
        elif response.status_code == 422: # user already is VIP
            return False, 422
        else:
            write_log(LOG_FILE, response.text)
            return False, response.status_code
    
    def create_poll(self, title, choices, duration):
        global ACCESS_TOKEN, request_headers

        uri = "https://api.twitch.tv/helix/polls"
        body = {
            "broadcaster_id": BROADCASTER_ID,
            "title": title,
            "choices": [{"title": choice} for choice in choices],
            "duration": duration,
            "channel_points_voting_enabled": False
        }

        response = requests.post(uri, headers=request_headers, json=body)

        if response.status_code == 401:
            try:
                ACCESS_TOKEN = refresh_access_token()
            except Exception as e:
                write_log(LOG_FILE, e)
                return
            
            request_headers["Authorization"] = f"Bearer {ACCESS_TOKEN}"
            response = requests.post(uri, headers=request_headers, json=body)

            if not response.ok:
                write_log(LOG_FILE, response.text)
                raise ConnectionError(f"Error creating poll. Error Details in {LOG_FILE}")
            
            return True
        
        elif response.status_code == 200:
            return True
        else:
            write_log(LOG_FILE, response.text)
            return False

    # get current twitch stream title
    def get_stream_title(self):
        global ACCESS_TOKEN, request_headers

        url = "https://api.twitch.tv/helix/channels"
        params = {
            "broadcaster_id": BROADCASTER_ID
        }

        response = requests.get(url, headers=request_headers, params=params)

        if response.status_code == 401:
            try:
                ACCESS_TOKEN = refresh_access_token()
                request_headers["Authorization"] = f"Bearer {ACCESS_TOKEN}"
            except ConnectionError as e:
                write_log(LOG_FILE, e)
                return
            
            response = requests.get(url, headers=request_headers, params=params)
            
            if not response.ok:
                write_log(LOG_FILE, response.text)

        try:
            data = response.json()["data"]
            stream_title = data[0]["title"]
            return stream_title
        except requests.exceptions.JSONDecodeError:
            write_log(LOG_FILE, response.text)

    # send patch request to update stream title
    def update_stream_title(self, new_stream_title):
        global ACCESS_TOKEN, request_headers

        url = "https://api.twitch.tv/helix/channels"
        params = {
            "broadcaster_id": BROADCASTER_ID
        }
        body = {
            "title": new_stream_title
        }

        response = requests.patch(url, headers=request_headers, params=params, json=body)

        if response.status_code == 401:
            try:
                ACCESS_TOKEN = refresh_access_token()
                request_headers["Authorization"] = f"Bearer {ACCESS_TOKEN}"
            except ConnectionError as e:
                write_log(LOG_FILE, e)
                return
            
            response = requests.patch(url, headers=request_headers, params=params)

        if "The request must update at least one channel property field." in response.text:
            write_log(LOG_FILE, f"NOTICE: {response.text}")

        if not response.ok:
            write_log(LOG_FILE, response.text)

    # update stream category to osu!
    def update_stream_category(self):
        global ACCESS_TOKEN, request_headers

        url = "https://api.twitch.tv/helix/channels"
        params = {
            "broadcaster_id": BROADCASTER_ID
            }
        body = {
            "game_id": "21465" # osu! ID in twitch backend
        }

        response = requests.patch(url, headers=request_headers, params=params, json=body)

        if response.status_code == 401:
            try:
                ACCESS_TOKEN = refresh_access_token()
                request_headers["Authorization"] = f"Bearer {ACCESS_TOKEN}"
            except ConnectionError as e:
                write_log(LOG_FILE, f"[ERROR]: {e}")
                return
            
            response = requests.patch(url, headers=request_headers, params=params, json=body)

        if not response.ok:
            write_log(LOG_FILE, response.text)

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
            write_log(LOG_FILE, e)
            
        except ValueError as e:
            write_log(LOG_FILE, f"NOTICE: {e}")

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