import websockets
import os
import json
import requests
from datetime import datetime as dt

from dotenv import load_dotenv
from bot.utils.refresh_access_token import refresh_access_token
from bot.utils.utils import write_log

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
BROADCASTER_ID = os.getenv("BROADCASTER_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

date_format = "%Y-%m-%d_%H-%M-%S"
LOG_FILE = f'logs/{dt.now().strftime(date_format)}.txt'

DEFAULT_URL = "wss://eventsub.wss.twitch.tv/ws"

# channel points redemption listener
async def eventsub_listener(redemption_handler, url=DEFAULT_URL, is_reconnect=False):
    global ACCESS_TOKEN

    async with websockets.connect(url) as ws:
        msg = await ws.recv()
        data = json.loads(msg)

        if data["metadata"]["message_type"] == "session_welcome":
            session_id = data["payload"]["session"]["id"]

        if not is_reconnect:
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
                    ACCESS_TOKEN = refresh_access_token()
                except Exception as e:
                    write_log(LOG_FILE, f"[ERROR] - Failed to refresh token: {e}")
                    return

                headers["Authorization"] = f"Bearer {ACCESS_TOKEN}"
                response = requests.post(
                    "https://api.twitch.tv/helix/eventsub/subscriptions",
                    headers=headers,
                    json=sub
                )

                if not response.ok: # if second try fails, stop trying to create subscription
                    write_log(LOG_FILE, f"[ERROR] - Failed to start Redemptions Listener: {response.text}")
                    return

        # wait for incoming notifications
        try:
            async for message in ws:
                data = json.loads(message)
                msg_type = data["metadata"]["message_type"]

                if msg_type == "notification":
                    event = data["payload"]["event"]
                    await redemption_handler(event)
                
                elif msg_type == "session_reconnect":
                    reconnect_url = data["payload"]["session"]["reconnect_url"]
                    write_log(LOG_FILE, f"[NOTICE] - Received EventSub session_reconnect, migrating to new session")
                    await eventsub_listener(redemption_handler, url=reconnect_url, is_reconnect=True)
                    return

                elif msg_type == "revocation":
                    revocation_reason = data["payload"]["status"]
                    write_log(LOG_FILE, f"[FATAL] - Redemptions Listener access revoked: {revocation_reason}")
                    await redemption_handler(msg_type)
        except Exception as e:
            write_log(LOG_FILE, f"[ERROR] - EventSub Listener failed: {e}")