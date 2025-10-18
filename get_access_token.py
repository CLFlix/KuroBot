import os
import requests
import time
from dotenv import load_dotenv, set_key

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
CODE = os.getenv("CODE")

def get_access_and_refresh_token():
    uri = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": CODE,
        "grant_type": "authorization_code",
        "redirect_uri": "http://localhost"
    }

    response = requests.post(uri, params=params)

    if response.status_code == 401:
        raise ConnectionError("Please try again with a newly generated code with the 'moderation:read' scope.")

    try:
        tokens = response.json()

        ACCESS_TOKEN, REFRESH_TOKEN = tokens["access_token"], tokens["refresh_token"]
        set_key(r'.env', "ACCESS_TOKEN", ACCESS_TOKEN)
        set_key(r'.env', "REFRESH_TOKEN", REFRESH_TOKEN)
        print("Retrieved access and refresh token from twitch and placed them in .env.")
        time.sleep(3)

    except requests.exceptions.JSONDecodeError:
        raise RuntimeError("Invalid or no response. The request has failed.")

get_access_and_refresh_token()