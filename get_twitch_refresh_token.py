import os
import requests

from dotenv import load_dotenv, set_key

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
CODE = os.getenv("CODE")

def get_refresh_token():
    uri = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": CODE,
        "grant_type": "authorization_code",
        "redirect_uri": "http:localhost"
    }
    response = requests.post(uri, params=params)

    if response.status_code == 401:
        raise ConnectionError("Double-check your credentials and try again. You might have to re-run 'get_twitch_refresh_token.py'. In that case, you don't have to run this one again.")

    try:
        tokens = response.json()

        ACCESS_TOKEN, REFRESH_TOKEN = tokens["access_token"], tokens["refresh_token"]
        set_key(r'.env', "BOT_ACCESS_TOKEN", ACCESS_TOKEN)
        set_key(r'.env', "BOT_REFRESH_TOKEN", REFRESH_TOKEN)
        
    except requests.exceptions.JSONDecodeError:
        print("Double-check your credentials and try again.")

get_refresh_token()
