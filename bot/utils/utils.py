from dotenv import load_dotenv

import requests
import os
import json
from datetime import datetime as dt
from datetime import timezone
from dateutil.relativedelta import relativedelta

load_dotenv()

osuUsername = os.getenv("osuUsername")
API_KEY = os.getenv("osuAuth")

# log errors to a file
def write_log(log_file, text: str):
    with open(log_file, 'a', encoding='utf-8') as log:
        log.write(f"{dt.now().strftime("%Y-%m-%d_%H-%M-%S")} - {text}\n")

def first_time_startup():
    # quick check if all files / log folder exist
    files = [r'first_time_bonus_claimed.txt', r'logs', r'points.json', r'socials.json']
    files_exist = [file in os.listdir(r'.') for file in files]
    if not all(files_exist):
        # create file to save all usernames that claimed first-time bonus
        # if it doesn't exist already
        if r'first_time_bonus_claimed.txt' not in os.listdir(r'.'):    
            with open("first_time_bonus_claimed.txt", 'w', encoding='utf-8') as bonus_claimed_file:
                bonus_claimed_file.write("")

        # create logs folder if it doesn't exist already
        if r'logs' not in os.listdir(r'.'):
            os.system("mkdir logs")

        # create file to save users' points if it doesn't exist already
        if r'points.json' not in os.listdir(r'.'):
            with open(r'points.json', 'w', encoding='utf-8') as points_file:
                json.dump({}, points_file)

        # create file for !socials command if it doesn't exist already
        if r'socials.json' not in os.listdir(r'.'):
            socials = {
                "YouTube": "",
                "Discord": "",
                "TikTok": "",
                "Instagram": "",
                "Twitter / X": "",
                "Linktree": ""
            }

            with open(r'socials.json', 'w', encoding='utf-8') as socials_file:
                json.dump(socials, socials_file, indent=4)

# load the socials links
def read_socials_links(socials_file):
    try:
        with open(socials_file, 'r', encoding='utf-8') as socials_json:
            socials = json.load(socials_json)
    except FileNotFoundError:
        return "No socials added"
    
    message_links = []
    for media, link in socials.items():
        if link:
            message_links.append(f"{media}: {link}") 

    return ", ".join(message_links) if message_links else "No socials added"

# When osuAuth and osuUsername are filled in in the .env file, this method can look up your osu! profile
def get_profile(user):
    profile_url = "https://osu.ppy.sh/api/get_user"
    params = {"k": API_KEY, "u": user}

    try:
        response = requests.get(url=profile_url, params=params)
    except:
        raise ConnectionError("osu! API is not reachable or request failed.")

    try:
        data = response.json()[0]
        return (True, data)
    except IndexError:
        return (False, "User not found")

# When you have StreamCompanion running, the command !np and !nppp will request the map through this method
# Since this endpoint is only called occasionally through !np, the
# performance impact of doing this instead of websockets should be irrelevant.
def get_map():
    companion_url = "http://localhost:20727/json"

    try:
        response = requests.get(companion_url)
    except:
        raise ConnectionError("StreamCompanion is not running or not accessible")
    
    response.encoding = 'utf-8-sig'
    data = response.json()
    return data

# receive mods and take away the comma
def format_mods(mods):
    if mods == "NM":
        formatted_mods = None
        return formatted_mods
    elif len(mods) > 2:
        formatted_mods = mods.replace(",", "")
        return formatted_mods
        
    return mods

# Get the points of every viewer
def get_points_data(points_file):
    with open(points_file, 'r', encoding='utf-8') as points:
        viewer_points = json.load(points)
    return viewer_points

# Save the points of all viewers
def write_points_data(viewer_points, points_file):
    with open(points_file, 'w', encoding='utf-8') as points_output:
        json.dump(viewer_points, points_output, indent=4)

def get_bonus_claimed(first_time_bonus_file):
    bonus_claimed = set()
    with open(first_time_bonus_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        bonus_claimed.add(line.strip())

    return bonus_claimed

def write_bonus_claimed(bonus_claimed_list, first_time_bonus_file):
    with open(first_time_bonus_file, 'w', encoding='utf-8') as file:
        for user in bonus_claimed_list:
            file.write(f"{user}\n")

def edit_stream_title(current_title: str, current_rank):
    open_bracket_index = current_title.find("[")
    close_bracket_index = current_title.find("]")

    if open_bracket_index == -1 or close_bracket_index == -1:
        new_title_rank = f"[#{current_rank}]"
        new_title = f"{new_title_rank} {current_title}"
        return new_title

    if current_rank in current_title[open_bracket_index + 1 : close_bracket_index]:
        raise ValueError("Didn't update title with the same rank, avoided crash.")

    new_title_rank = f"[#{current_rank}]"
    new_title = current_title.replace(current_title[open_bracket_index : close_bracket_index + 1], new_title_rank)
    
    return new_title

def calculate_followage_days(followed_at):
    start = dt.strptime(followed_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    now = dt.now(timezone.utc)

    rd = relativedelta(now, start)

    parts = []
    if rd.years:
        parts.append(f"{rd.years} year{'s' if rd.years != 1 else ''}")
    if rd.months:
        parts.append(f"{rd.months} month{'s' if rd.months != 1 else ''}")
    if rd.days:
        parts.append(f"{rd.days} day{'s' if rd.days != 1 else ''}")
    if rd.hours:
        if rd.minutes > 30:
            rd.hours += 1
        parts.append(f"{rd.hours} hour{'s' if rd.hours != 1 else ''}")

    return " ".join(parts) if parts else "less than an hour"