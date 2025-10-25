import websockets
import os
import json
import requests

from dotenv import load_dotenv
from refresh_access_token import refresh_access_token
from utils import log_error

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
BROADCASTER_ID = os.getenv("BROADCASTER_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

# channel points redemption listener
async def eventsub_listener(redemption_handler):
    url = "wss://eventsub.wss.twitch.tv/ws"

    async with websockets.connect(url) as ws:
        msg = await ws.recv()
        data = json.loads(msg)

        if data["metadata"]["message_type"] == "session_welcome":
            session_id = data["payload"]["session"]["id"]

            headers = {
                    "Authorization": f"Bearer {ACCESS_TOKEN}",
                    "Client-Id": CLIENT_ID,
                    "Content-Type": "application/json"
                }

            sub = {
                "type": "channel.channel_points_custom_reward_redemption.add",
                "version": "1",
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

                try:
                    # refresh access token for redemption listener, then retry subscription
                    new_token = refresh_access_token()
                except Exception as e:
                    print(f"Token refresh failed, details in log.txt")
                    log_error(r'log.txt', e)
                    return

                headers["Authorization"] = f"Bearer {new_token}"
                response = requests.post(
                    "https://api.twitch.tv/helix/eventsub/subscriptions",
                    headers=headers,
                    json=sub
                )

                if response.status_code not in (200, 202): # if second try fails, stop trying to create subscription
                    print(f"Second try to create EventSub Listener failed. Details in log.txt")
                    log_error(r'log.txt', response.text)
                    return
                
        print("Listening for redemptions...")
        
        # wait for incoming notifications
        try:
            async for message in ws:
                data = json.loads(message)
                msg_type = data["metadata"]["message_type"]

                if msg_type == "notification":
                    event = data["payload"]["event"]
                    await redemption_handler(event)
                elif msg_type == "revocation":
                    revocation_reason = data["payload"]["status"]
                    print(f"The redemption subscription has been revoked. Details in log.txt")
                    log_error(r'log.txt', revocation_reason)
                    await redemption_handler(msg_type)
        except Exception as e:
            print(f"EventSub Listener crashed: details in log.txt")
            log_error(r'log.txt', e)