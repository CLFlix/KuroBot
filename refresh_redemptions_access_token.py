import os
import requests
from dotenv import load_dotenv, set_key

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN_REDEMPTIONS = os.getenv("REFRESH_TOKEN_REDEMPTIONS")

def refresh_token_redemptions():
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN_REDEMPTIONS,
        "grant_type": "refresh_token"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise RuntimeError(f"Failed to refresh: {response.text}")

    tokens = response.json()
    NEW_ACCESS_TOKEN, NEW_REFRESH_TOKEN = tokens["access_token"], tokens["refresh_token"]

    set_key(r'.env', "ACCESS_TOKEN_REDEMPTIONS", NEW_ACCESS_TOKEN)
    set_key(r'.env', "REFRESH_TOKEN_REDEMPTIONS", NEW_REFRESH_TOKEN)

    return NEW_ACCESS_TOKEN
