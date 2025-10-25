from dotenv import load_dotenv

import requests
import os
import json
from datetime import datetime as dt

load_dotenv()

osuUsername = os.getenv("osuUsername")
API_KEY = os.getenv("osuAuth")

# wipe log file
def clean_logs(log_file):
    with open(log_file, 'w', encoding='utf-8') as logs:
        logs.write("")

# log errors to a file
def log_error(log_file, error):
    with open(log_file, 'a', encoding='utf-8') as logs:
        logs.write(f"{dt.now()} - {error}")
    print(f"{dt.now()} Error logged in {log_file}\n")

# When osuAuth and osuUsername are filled in in the .env file, this method can look up your osu! profile
def get_profile():
    profile_url = "https://osu.ppy.sh/api/get_user"
    params = {"k": API_KEY, "u": osuUsername}

    try:
        response = requests.get(url=profile_url, params=params)
    except:
        raise ConnectionError("osu! API is not reachable or request failed.")

    data = response.json()[0]
    return data

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
    formatted_mods = mods

    if formatted_mods == "NM":
        formatted_mods = None
    elif len(formatted_mods) > 2:
        formatted_mods = formatted_mods.replace(",", "")
    
    return formatted_mods

# Get the points of every viewer
def get_points_data(points_file):
    try:
        with open(points_file, 'r', encoding='utf-8') as points:
            viewer_points = json.load(points)
    except FileNotFoundError: # first time startup
        viewer_points = {}
        with open(points_file, 'w', encoding='utf-8') as points:
            points.write("{}")
    return viewer_points

# Save the points of all viewers
def write_points_data(viewer_points, points_file):
    with open(points_file, 'w', encoding='utf-8') as points_output:
        json.dump(viewer_points, points_output, indent=4)
    print("Points data saved!")

def get_bonus_claimed(first_time_bonus_file):
    bonus_claimed = []
    try:
        with open(first_time_bonus_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        for line in lines:
            bonus_claimed.append(line.strip().lower())

    except FileNotFoundError:
        with open("first_time_bonus_claimed.txt", 'w', encoding='utf-8') as bonus_claimed_file:
            bonus_claimed_file.write("")
    return bonus_claimed

def write_bonus_claimed(bonus_claimed_list, first_time_bonus_file):
    with open(first_time_bonus_file, 'w', encoding='utf-8') as file:
        for user in bonus_claimed_list:
            file.write(f"{user}\n")
    print("First time bonus data saved!")

def edit_stream_title(current_title: str, current_rank):
    open_bracket_index = current_title.find("[")
    close_bracket_index = current_title.find("]")

    if open_bracket_index == -1 or close_bracket_index == -1:
        raise SyntaxError("Title malformed, there is no rank between brackets - [] - in the title.")

    if current_rank in current_title[open_bracket_index + 1 : close_bracket_index]:
        raise ValueError("Didn't update title with the same rank, avoided crash.")

    new_title_rank = f"#{current_rank}"
    new_title = current_title.replace(current_title[open_bracket_index + 1 : close_bracket_index], new_title_rank)
    
    return new_title

def calculate_followage_days(followed_at):
    dt_followed_at = dt.strptime(followed_at, "%Y-%m-%dT%H:%M:%SZ")
    days_total = (dt.now() - dt_followed_at).days
    years, days = divmod(days_total, 365)

    parts = []
    if years:
        parts.append(f"{years} year{'s' if years != 1 else ''}")
    if days:
        parts.append(f"{days} day{'s' if days != 1 else ''}")

    return " ".join(parts) or ""