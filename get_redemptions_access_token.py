from dotenv import load_dotenv, set_key

import os
import requests

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
CODE_REDEMPTIONS = os.getenv("CODE_REDEMPTIONS")

def get_redemptions_access_and_refresh_token():
    uri = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": CODE_REDEMPTIONS,
        "grant_type": "authorization_code",
        "redirect_uri": "http://localhost"
    }

    response = requests.post(uri, params=params)

    if response.status_code == 401:
        raise ConnectionError("This error comes from the redemptions listener. Please check your credentials.")
    

    try:
        data = response.json()

        ACCESS_TOKEN, REFRESH_TOKEN = data["access_token"], data["refresh_token"]
        print(ACCESS_TOKEN, REFRESH_TOKEN)
        set_key(r'.env', "ACCESS_TOKEN_REDEMPTIONS", ACCESS_TOKEN)
        set_key(r'.env', "REFRESH_TOKEN_REDEMPTIONS", REFRESH_TOKEN)

    except requests.exceptions.JSONDecodeError:
        raise RuntimeError("Invalid or no response. The request has failed.")

get_redemptions_access_and_refresh_token()
