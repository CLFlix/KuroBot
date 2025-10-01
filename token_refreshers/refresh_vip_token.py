import os
import requests
from dotenv import load_dotenv, set_key

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN_VIP = os.getenv("REFRESH_TOKEN_VIP")

def refresh_tokens():
    response = requests.post("https://id.twitch.tv/oauth2/token",
                            data={
                                "client_id": CLIENT_ID,
                                "client_secret": CLIENT_SECRET,
                                "grant_type": "refresh_token",
                                "refresh_token": REFRESH_TOKEN_VIP
                            })

    if response.status_code != 200:
        raise RuntimeError(f"Failed to refresh: {response.text}")

    tokens = response.json()
    NEW_ACCESS_TOKEN = tokens["access_token"]
    NEW_REFRESH_TOKEN = tokens["refresh_token"]

    set_key(r'.env', "ACCESS_TOKEN_VIP", NEW_ACCESS_TOKEN)
    set_key(r'.env', "REFRESH_TOKEN_VIP", NEW_REFRESH_TOKEN)

    return NEW_ACCESS_TOKEN
