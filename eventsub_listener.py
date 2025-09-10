import websockets
import os
import json
import requests

from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
BROADCASTER_ID = os.getenv("BROADCASTER_ID")
CODE_SCOPE_REDEMPTIONS = os.getenv("CODE_SCOPE_REDEMPTIONS")

# Not the same token as BOT_ACCESS_TOKEN
def get_app_token():
    response = requests.post(
        "https://id.twitch.tv/oauth2/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "client_credentials"
        }
    )
    response.raise_for_status()
    return response.json()["access_token"]

# channel points redemption listener
async def eventsub_listener():
    url = "wss://eventsub.wss.twitch.tv/ws"

    async with websockets.connect(url) as ws:
        print("Connected to Twitch EventSub WebSocket")

        msg = await ws.recv()
        data = json.loads(msg)

        if data["metadata"]["message_type"] == "session_welcome":
            print("Received session_welcome from Twitch")
            session_id = data["payload"]["session"]["id"]

            sub = {
                "type": "channel.channel_points_custom_reward_redemption.add",
                "version": 1,
                "condition": {"broadcaster_user_id": BROADCASTER_ID},
                "transport": {
                    "method": "websocket",
                    "session_id": session_id
                }
            }

            response = requests.post(
                "https://api.twitch.tv/helix/eventsub/subscriptions",
                headers={
                    "Authorization": f"Bearer {CODE_SCOPE_REDEMPTIONS}",
                    "Client-Id": CLIENT_ID,
                    "Content-Type": "application/json"
                },
                json=sub
            )

            print("Subscription response:", response.status_code, response.text)
        
        # wait for incoming notifications
        async for message in ws:
            data = json.loads(message)
            msg_type = data["metadata"]["message_type"]

            if msg_type == "notification":
                print(message)
                # handler function coming later (in main)
            elif msg_type == "session_keepalive":
                print("Received keepalive message\nREMOVE THIS FOR PRODUCTION")
