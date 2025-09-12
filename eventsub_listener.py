import websockets
import os
import json
import requests

from dotenv import load_dotenv
from refresh_redemptions_access_token import refresh_token_redemptions

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
BROADCASTER_ID = os.getenv("BROADCASTER_ID")
ACCESS_TOKEN_REDEMPTIONS = os.getenv("ACCESS_TOKEN_REDEMPTIONS")

# channel points redemption listener
async def eventsub_listener(redemption_handler):
    global ACCESS_TOKEN_REDEMPTIONS
    url = "wss://eventsub.wss.twitch.tv/ws"

    async with websockets.connect(url) as ws:
        print("Connected to Twitch EventSub WebSocket")

        msg = await ws.recv()
        data = json.loads(msg)

        if data["metadata"]["message_type"] == "session_welcome":
            print("Received session_welcome from Twitch")
            session_id = data["payload"]["session"]["id"]

            headers = {
                    "Authorization": f"Bearer {ACCESS_TOKEN_REDEMPTIONS}",
                    "Client-Id": CLIENT_ID,
                    "Content-Type": "application/json"
                }

            sub = {
                "type": "channel.channel_points_custom_reward_redemption.add",
                "version": 1,
                "condition": {"broadcaster_user_id": BROADCASTER_ID},
                "transport": {
                    "method": "websocket",
                    "session_id": session_id
                }
            }

            # initial try to create subscription
            response = requests.post(
                "https://api.twitch.tv/helix/eventsub/subscriptions",
                headers=headers,
                json=sub
            )

            if response.status_code == 401:
                print("EventSub Listener couldn't connect. Retrying once...")

                try:
                    # refresh access token for redemption listener, then retry subscription
                    ACCESS_TOKEN_REDEMPTIONS = refresh_token_redemptions()
                    print("Refreshed redemption listener token")
                except Exception as e:
                    print(f"Refresh failed: {e}")
                    return

                response = requests.post(
                    "https://api.twitch.tv/helix/eventsub/subscriptions",
                    headers=headers,
                    json=sub
                )

                if response.status_code != 200: # if second try fails, stop trying to create subscription
                    print(f"Second try to create EventSub Listener failed. This part of the bot won't work this session. Response: {response.text}")
                    return
                
        print("Listening for redemptions...")
        
        # wait for incoming notifications
        async for message in ws:
            data = json.loads(message)
            msg_type = data["metadata"]["message_type"]

            if msg_type == "notification":
                event = data["payload"]["event"]
                redemption_handler(event)
            elif msg_type == "revocation":
                revocation_reason = data["payload"]["status"]
                print(f"The redemption subscription has been revoked. Reason: {revocation_reason}")
                redemption_handler(msg_type)