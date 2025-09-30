import os
import requests

from dotenv import load_dotenv, set_key

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
CODE_POLLS = os.getenv("CODE_POLLS")

def get_polls_access_and_refresh_token():
    uri = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": CODE_POLLS,
        "grant_type": "authorization_code",
        "redirect_uri": "http://localhost"
    }

    response = requests.post(uri, params=params)

    if response.status_code == 401:
        raise ConnectionError("Please try again with a newly generated code with the 'channel:manage:polls' scope.")

    try:
        tokens = response.json()

        ACCESS_TOKEN, REFRESH_TOKEN = tokens["access_token"], tokens["refresh_token"]
        set_key(r'.env', "ACCESS_TOKEN_POLLS", ACCESS_TOKEN)
        set_key(r'.env', "REFRESH_TOKEN_POLLS", REFRESH_TOKEN)
    
    except requests.exceptions.JSONDecodeError:
        raise RuntimeError("Invalid or no response. The request has failed.")

get_polls_access_and_refresh_token()
