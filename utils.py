from dotenv import load_dotenv

import requests
import os
import json

load_dotenv()

osuUsername = os.getenv("osuUsername")
API_KEY = os.getenv("osuAuth")

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

# Get the points of every viewer
def get_points_data(points_file):
    with open(points_file, 'r', encoding='utf-8') as points:
        viewer_points = json.load(points)
    return viewer_points

# Save the points of all viewers
def write_points_data(viewer_points, points_file):
    with open(points_file, 'w', encoding='utf-8') as points_output:
        json.dump(viewer_points, points_output, indent=4)
    print("Points data saved!")

def get_bonus_claimed(first_time_bonus_file):
    with open(first_time_bonus_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    bonus_claimed = []
    for line in lines:
        bonus_claimed.append(line.strip().lower())

    return bonus_claimed

def write_bonus_claimed(bonus_claimed_list, first_time_bonus_file):
    with open(first_time_bonus_file, 'w', encoding='utf-8') as file:
        file.writelines(bonus_claimed_list)
    print("First time bonus data saved!")
