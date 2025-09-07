import requests
import os
from dotenv import load_dotenv, set_key

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
CODE = os.getenv("CODE")
REDIRECT_URI = "http://localhost"

def get_refresh_token():
    response = requests.post("https://id.twitch.tv/oauth2/token",
                            data={
                                "client_id": CLIENT_ID,
                                "client_secret": CLIENT_SECRET,
                                "code": CODE,
                                "grant_type": "authorization_code",
                                "redirect_uri": REDIRECT_URI
                            }
                        )

    try:
        tokens = response.json()

        ACCESS_TOKEN = tokens["access_token"]
        REFRESH_TOKEN = tokens["refresh_token"]

        set_key(r'.env', "BOT_ACCESS_TOKEN", ACCESS_TOKEN)
        set_key(r'.env', "BOT_REFRESH_TOKEN", REFRESH_TOKEN)
    except requests.exceptions.JSONDecodeError:
        print("Double-check your credentials and try again.")

get_refresh_token()
