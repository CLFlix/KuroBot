import os
import time
import requests
from dotenv import load_dotenv, set_key

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TWITCH_LOGIN = os.getenv("CHANNEL")

def get_broadcaster_id_token():
    url = "https://id.twitch.tv/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }

    response = requests.post(url, headers=headers, data=data)

    if not response.ok:
        raise ConnectionError("Client ID or Client Secret is not valid. Please confirm on the Twitch Developers Dashboard if these are right and refresh if necessary.")

    try:
        token = response.json()["access_token"]
        return token
    except requests.exceptions.JSONDecodeError as e:
        print(e + "\n\n", "Please try again with a new client ID / secret. If the issue persists, open an issue on the GitHub page: https://github.com/CLFlix/KuroBot/issues")
        time.sleep(30)
        return
    
def get_broadcaster_id():
    token = get_broadcaster_id_token()

    if not token:
        return
    
    url = f"https://api.twitch.tv/helix/users?login={TWITCH_LOGIN}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Client-Id": CLIENT_ID
    }

    response = requests.get(url, headers=headers)

    if not response.ok:
        raise ConnectionError(f"Something went wrong, please contact the developer on GitHub with the following error text: https://github.com/CLFlix/KuroBot/issues\n{response.text}")

    try:
        data = response.json()["data"]
        broadcaster_id = data[0]["id"]

        set_key(r'.env', "BROADCASTER_ID", broadcaster_id)
        print("Placed broadcaster ID in .env")
        time.sleep(3)

    except requests.exceptions.JSONDecodeError as e:
        print(f"Something went wrong. Please open an issue so the developer can fix this ASAP: https://github.com/CLFlix/KuroBot/issues\n{e}")
        print("Visible for 30 seconds")
        time.sleep(30)
        return
    
get_broadcaster_id()
