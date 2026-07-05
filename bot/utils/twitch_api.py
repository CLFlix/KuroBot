import os
import requests

from bot.utils.refresh_access_token import refresh_access_token
from bot.utils.utils import write_log, write_original_vips

CLIENT_ID = os.getenv("CLIENT_ID")
BROADCASTER_ID = os.getenv("BROADCASTER_ID")

class TwitchAPI:
    def __init__(self, access_token, log_file):
        self.access_token = access_token
        self.log_file = log_file
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Client-Id": CLIENT_ID,
            "Content-Type": "application/json"
        }

    def _refresh(self):
        try:
            self.access_token = refresh_access_token()
            self.headers["Authorization"] = f"Bearer {self.access_token}"
            write_log(self.log_file, "[INFO] - Refreshed Access Token")
            return True
        except Exception as e:
            write_log(self.log_file, f"[ERROR] - Couldn't refresh access token: {e}")
            return False
    
    def _request(self, method, url, **kwargs):
        response = requests.request(method, url, headers=self.headers, **kwargs)

        if response.status_code == 401 and self._refresh():
            response = requests.request(method, url, headers=self.headers, **kwargs)

        log_url = url.replace("https://api.twitch.tv/helix/", "")

        if response.ok:
            write_log(self.log_file, f"[INFO] - Received response from '{log_url}'")
            return response

        write_log(self.log_file, f"[WARN] - Could not get valid response from '{log_url}': {response.text}")
    
    def get_mods_list(self, bot_nick):
        uri = "https://api.twitch.tv/helix/moderation/moderators"
        params = {"broadcaster_id": BROADCASTER_ID}

        response = self._request("get", uri, params=params)

        if response.status_code != 200:
            write_log(self.log_file, f"[ERROR] - Couldn't get mods list: {response.text}")
            raise ConnectionError(f"Error getting mods list. More detailed error in {self.log_file}")

        try:
            data = response.json()["data"]
            mods_list = [mod["user_login"] for mod in data]

            with open("mods_list.txt", 'w', encoding='utf-8') as mods_file:
                for mod in mods_list:
                    mods_file.write(f"{mod}\n")
                mods_file.write(bot_nick)
        
        except requests.exceptions.JSONDecodeError:
            raise RuntimeError("Couldn't get moderators")

    def get_banned_users(self):
        uri = "https://api.twitch.tv/helix/moderation/banned"
        params = {"broadcaster_id": BROADCASTER_ID}

        response = self._request("get", uri, params=params)
        
        if response.status_code != 200:
            write_log(self.log_file, f"[ERROR] - Couldn't get banned users: {response.text}")
            raise ConnectionError("Couldn't get banned users.")

        try:
            data = response.json()["data"]
            banned_users = set()
            for banned_user in data:
                banned_users.add(banned_user["user_login"])
            return banned_users
        except requests.exceptions.JSONDecodeError as e:
            write_log(self.log_file, f"[ERROR] - Couldn't decode banned users list: {e}")
    
    def user_exists(self, username) -> bool:
        url = f"https://api.twitch.tv/helix/users?login={username}"
        response = self._request("get", url)

        if not response.ok:
            write_log(self.log_file, f"[ERROR] - Couldn't get user data: {response.text}")
            return False

        data = response.json()
        return len(data["data"]) > 0
    
    def get_user_id(self, user):
        url = "https://api.twitch.tv/helix/users"
        params = {"login": user}

        response = self._request("get", url, params=params)

        try:
            user_data = response.json()
            return user_data["data"][0]["id"]
        except requests.exceptions.JSONDecodeError as e:
            write_log(self.log_file, f"[ERROR] - Couldn't get user ID: {e}")

    def get_follower_data(self, user_id):
        url = "https://api.twitch.tv/helix/channels/followers"
        params = {
            "user_id": user_id,
            "broadcaster_id": BROADCASTER_ID
        }

        response = self._request("get", url, params=params)

        if not response.ok:
            write_log(self.log_file, f"[ERROR] - Couldn't get follower data: {response.text}")
            return

        try:
            data = response.json()["data"]
            if not data:
                return
            return data[0]["followed_at"]
        except requests.exceptions.JSONDecodeError as e:
            write_log(self.log_file, f"[ERROR] - Invalid or no response getting followage: {e}")

    def get_vip_list(self):
        with open(r'vips.json', 'r', encoding='utf-8') as vips_file:
            if len(vips_file.read()) != 2: # if the dict is empty, then the char amount is 2: '{}'
                return

        url = "https://api.twitch.tv/helix/channels/vips"
        params = {
            "broadcaster_id": BROADCASTER_ID,
            "first": 100
        }
        
        try:
            response = self._request("get", url, params=params)
        except ConnectionError as e:
            write_log(self.log_file, f"[ERROR] - Something went wrong getting VIPs: {e}")

        if not response.ok:
            write_log(self.log_file, f"[ERROR] - Something went wrong getting VIPs: {response.text}")
            return
        
        try:
            data = response.json()["data"]
            write_original_vips(data)
            write_log(self.log_file, f"[INFO] - Written original VIPs list to vips.json")
        except requests.exceptions.JSONDecodeError as e:
            write_log(self.log_file, f"[ERROR] - Invalid or no response getting vips list: {e}")

    def add_vip(self, user_id):
        url = "https://api.twitch.tv/helix/channels/vips"
        params = {
            "broadcaster_id": BROADCASTER_ID,
            "user_id": user_id
        }

        try:
            response = self._request("post", url, params=params)
        except ConnectionError:
            return "Something went wrong assigning VIP status.."

        if response.status_code == 204:
            return True, 204
        elif response.status_code == 422:  # user already is VIP
            return False, 422
        else:
            write_log(self.log_file, f"[ERROR] - Couldn't add VIP to user {user_id}: {response.text}")
            return False, response.status_code

    # --- Polls ---

    def create_poll(self, title, choices, duration):
        uri = "https://api.twitch.tv/helix/polls"
        body = {
            "broadcaster_id": BROADCASTER_ID,
            "title": title,
            "choices": [{"title": choice} for choice in choices],
            "duration": duration,
            "channel_points_voting_enabled": False
        }

        response = self._request("post", uri, json=body)

        if response.status_code == 200:
            return True
        else:
            write_log(self.log_file, f"[ERROR] - Couldn't create poll: {response.text}")
            return False

    # --- Channel / stream ---

    def get_stream_title(self):
        url = "https://api.twitch.tv/helix/channels"
        params = {"broadcaster_id": BROADCASTER_ID}

        response = self._request("get", url, params=params)

        if not response.ok:
            write_log(self.log_file, f"[ERROR] - Couldn't get stream title: {response.text}")

        try:
            data = response.json()["data"]
            return data[0]["title"]
        except requests.exceptions.JSONDecodeError as e:
            write_log(self.log_file, f"[ERROR] - Couldn't decode stream title response: {e}")

    def update_stream_title(self, new_stream_title):
        url = "https://api.twitch.tv/helix/channels"
        params = {"broadcaster_id": BROADCASTER_ID}
        body = {"title": new_stream_title}

        response = self._request("patch", url, params=params, json=body)

        if "The request must update at least one channel property field." in response.text:
            write_log(self.log_file, f"[NOTICE] - {response.text}")

        if not response.ok:
            write_log(self.log_file, f"[ERROR] - Couldn't update stream title: {response.text}")

    def update_stream_category(self):
        url = "https://api.twitch.tv/helix/channels"
        params = {"broadcaster_id": BROADCASTER_ID}
        body = {"game_id": "21465"}  # osu! ID in twitch backend

        response = self._request("patch", url, params=params, json=body)

        if not response.ok:
            write_log(self.log_file, f"[ERROR] - Couldn't update stream category: {response.text}")