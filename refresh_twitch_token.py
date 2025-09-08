import os
import requests
from dotenv import load_dotenv, set_key

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("BOT_REFRESH_TOKEN")

def refresh_tokens():
    response = requests.post("https://id.twitch.tv/oauth2/token",
                            data={
                                "client_id": CLIENT_ID,
                                "client_secret": CLIENT_SECRET,
                                "grant_type": "refresh_token",
                                "refresh_token": REFRESH_TOKEN
                            })

    if response.status_code != 200:
        raise RuntimeError(f"Failed to refresh: {response.text}")

    tokens = response.json()
    NEW_ACCESS_TOKEN = tokens["access_token"]
    NEW_REFRESH_TOKEN = tokens["refresh_token"]

    set_key(r'.env', "BOT_ACCESS_TOKEN", NEW_ACCESS_TOKEN)
    set_key(r'.env', "BOT_REFRESH_TOKEN", NEW_REFRESH_TOKEN)

    global BOT_ACCESS_TOKEN
    return NEW_ACCESS_TOKEN
