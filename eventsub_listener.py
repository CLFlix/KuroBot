import websockets
import os
import json
import requests

from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
BROADCASTER_ID = os.getenv("BROADCASTER_ID")

# Not the same token as BOT_ACCESS_TOKEN
def get_app_token():
    response = requests.post("https://id.twitch.tv/oauth2/token", {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    })
    response.raise_for_status()
    return response.json()["access_token"]

# channel points redemption listener
async def eventsub_listener():
    EVENTSUB_TOKEN = get_app_token()
    url = "wss://eventsub.wss.twitch.tv/ws"

    async with websockets.connect(url) as ws:
        print("Connected to Twitch EventSub WebSocket")

        msg = await ws.recv()
        data = json.loads(msg)

        if data["metadata"]["message_type"] == "session_welcome":
            print("Received session_welcome from Twitch")
            topic = f"channel.channel_points_custom_reward_redemption.add.{BROADCASTER_ID}"
            payload = {
                "type": "LISTEN",
                "nonce": "unique_nonce",
                "data": {
                    "topics": [topic],
                    "auth_token": EVENTSUB_TOKEN
                }
            }
            await ws.send(json.dumps(payload))
            print("LISTEN sent to Twitch")

        async for message in ws:
            data = json.loads(message)
            if data["metadata"]["message_type"] == "notification":
                print(message)
                # handler function coming later (in main)
