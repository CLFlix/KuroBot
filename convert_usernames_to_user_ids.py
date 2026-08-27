from bot.utils.refresh_access_token import refresh_access_token
from bot.utils.utils import write_log

from dotenv import load_dotenv
import os
import requests
import json
import time

load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
BROADCASTER_ID = os.getenv("BROADCASTER_ID")

LOG_FILE = "logs/conversion_log.txt"

def read_user_points_file():
    with open(r'points.json', 'r', encoding="utf-8") as points_file:
        points = json.load(points_file)
    return points

def write_new_points_file(points_data):
    if BROADCASTER_ID in points_data.keys():
        del points_data[BROADCASTER_ID]
    with open(r'./points_ids.json', 'w', encoding='utf-8') as points_file:
        json.dump(points_data, points_file, indent=4)

def read_first_time_bonus():
    with open(r'first_time_bonus_claimed.txt', 'r', encoding='utf-8') as bonus_file:
        bonus_claimed_users = bonus_file.readlines()
    return bonus_claimed_users

def write_new_first_time_bonus(bonus_claimed_users_ids):
    with open(r'first_time_bonus_claimed_ids.txt', 'w', encoding='utf-8') as bonus_file:
        for bonus_claimed_user_id in bonus_claimed_users_ids:
            bonus_file.write(bonus_claimed_user_id + "\n")

def _request_user_id(username):
    global ACCESS_TOKEN
    url = "https://api.twitch.tv/helix/users"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Client-Id": CLIENT_ID,
        "Content-Type": "application/json"
    }
    params = {"login": username}

    res = requests.get(url=url, headers=headers, params=params)

    if res.status_code == 401:
                ACCESS_TOKEN = refresh_access_token()
                headers["Authorization"] = f"Bearer {ACCESS_TOKEN}"
    
                res = requests.get(url=url, headers=headers, params=params)
    
    if not res.ok:
        write_log(LOG_FILE, f"[WARN] - Skipping {username} because of bad request")
        print(f"[WARN] - Skipping {username} because of bad request")
        return False

    return res.json()

def convert_points():
    user_points = read_user_points_file()

    user_points_with_ids = {}

    for username, points in user_points.items():
        res = _request_user_id(username)
        data = res["data"]

        if len(data) > 0:
            user_id = data[0]["id"]
            user_points_with_ids[user_id] = points

        write_log(LOG_FILE, f"[INFO] - Finished converting {username} to user ID")
        print(f"[INFO] - Finished converting {username} to user ID")

    write_log(LOG_FILE, "[INFO] - Finished converting points.json to points_ids.json")
    write_new_points_file(user_points_with_ids)
    print("[INFO] - Finished converting points.json to points_ids.json\nStarting first_time_bonus_claimed.txt conversion in 3 seconds")
    time.sleep(3)


def convert_first_time_bonus():
    bonus_claimed_users = read_first_time_bonus()
    bonus_claimed_users_ids = []

    for username in bonus_claimed_users:
        username = username.removesuffix("\n")
        res = _request_user_id(username)

        if not res:
            continue


        data = res["data"]
        if len(data) > 0:
            user_id = data[0]["id"]
            bonus_claimed_users_ids.append(user_id)

            write_log(LOG_FILE, f"[INFO] - Finished converting {username} to user ID")
            print(f"[INFO] - Finished converting {username} to user ID")

    write_new_first_time_bonus(bonus_claimed_users_ids)
    write_log(LOG_FILE, f"[INFO] - Finished converting first_time_bonus_claimed.txt to first_time_bonus_claimed_ids.txt")

convert_points()
convert_first_time_bonus()

print("New files points_ids.json & first_time_bonus_claimed_ids.txt have been made! You can now remove the old ones and remove the '_ids' part of the new file names.")
print("Log file can be found in the logs folder (it has a distinct name)")
print("This window will close in 10 seconds")

time.sleep(10)
