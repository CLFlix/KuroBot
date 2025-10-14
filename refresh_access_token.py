import os
import requests
from dotenv import load_dotenv, set_key

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

REFRESH_TOKEN_VIP = os.getenv("REFRESH_TOKEN_VIP")
REFRESH_TOKEN_POLLS = os.getenv("REFRESH_TOKEN_POLLS")
REFRESH_TOKEN_REDEMPTIONS = os.getenv("REFRESH_TOKEN_REDEMPTIONS")
REFRESH_TOKEN_MODS = os.getenv("REFRESH_TOKEN_MODS")

def refresh_access_token(token_type: str):
    match token_type.lower():
        case "vip":
            REFRESH_TOKEN = REFRESH_TOKEN_VIP
            ACCESS_TOKEN_FIELD, REFRESH_TOKEN_FIELD = "ACCESS_TOKEN_VIP", "REFRESH_TOKEN_VIP"
        case "polls":
            REFRESH_TOKEN = REFRESH_TOKEN_POLLS
            ACCESS_TOKEN_FIELD, REFRESH_TOKEN_FIELD = "ACCESS_TOKEN_POLLS", "REFRESH_TOKEN_POLLS"
        case "redemptions":
            REFRESH_TOKEN = REFRESH_TOKEN_REDEMPTIONS
            ACCESS_TOKEN_FIELD, REFRESH_TOKEN_FIELD = "ACCESS_TOKEN_REDEMPTIONS", "REFRESH_TOKEN_REDEMPTIONS"
        case "mods":
            REFRESH_TOKEN = REFRESH_TOKEN_MODS
            ACCESS_TOKEN_FIELD, REFRESH_TOKEN_FIELD = "ACCESS_TOKEN_MODS", "REFRESH_TOKEN_MODS"

    uri = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token"
    }

    response = requests.post(uri, params=params)

    if response.status_code != 200:
        raise RuntimeError(f"Failed to refresh token: {response.text}")

    tokens = response.json()
    NEW_ACCESS_TOKEN, NEW_REFRESH_TOKEN = tokens["access_token"], tokens["refresh_token"]
    set_key(r'.env', ACCESS_TOKEN_FIELD, NEW_ACCESS_TOKEN)
    set_key(r'.env', REFRESH_TOKEN_FIELD, NEW_REFRESH_TOKEN)

    return NEW_ACCESS_TOKEN

