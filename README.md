# KuroBot

## Installation

### For developers:

Before being able to run anything, you need to install some dependencies in order for the script to work. Open command prompt and navigate to this folder and run:

```
pip install -r requirements.txt
```

---

### All users:

You will need <a href="https://github.com/Piotrekol/StreamCompanion">StreamCompanion</a> in order for `!np` and `!nppp` to work. This bot uses localhost:20727 to get the map's information.

## Account and Authorization

You will need to fill in some fields in a `.env` file within this folder:

The `CHANNEL` field has to be filled with the channel you want the bot to chat in, if you use it normally, this will be your own channel name.\
`TOKEN` will be your account token to essentially log your bot into your account to chat. You can easily find this token by going to Twitch on your browser and opening the `Network` tab in F12. Then you look for any `gql` entry. If you don't see any pop up, simply refresh the page and you should see them coming in. Click on the entry and look for `Authorization` in the `Headers` section. The value will be `OAuth YOUROAUTHTOKEN`.\
`osuUsername` is self-explanatory.\
`osuAuth` is the authorization key you need for any request to the osu! API. You can find the details on how to get this on the bottom of your osu! account settings page.\
**The following are optional if you want to be able to assign VIP status, create polls and listen to redemptions through the bot. This won't work without these values.**\
First of all you'll need a **client ID** and a **client secret** of a Twitch Application, so you can contact the twitch API.

---

1. Go to [Twitch Developer Console --> Applications](https://dev.twitch.tv/console/apps)
2. Log in
3. Register your bot. You can give it any name you want as long as it's valid. The redirect URL **should** be set to `http:localhost`. Category: Chat Bot
4. After creating, click "Manage" on your freshly registered app and copy the client ID in the `.env` file with the variable name "CLIENT_ID".
5. You will also need a client secret, which you can find further down. Create a new secret and copy that over to the `.env` file with the variable name "CLIENT_SECRET".

---

The bot will also need your broadcaster ID to be able to do some things on your channel, otherwise it doesn't know what channel to read your mods list (!polls), read your followers list (!followage),... You can run the "GetBroadcasterId.exe" for that, since it's fully automated now!

---

_Notice: The next and last thing you need can be done in 2 ways. I'm using the long-term setup, otherwise you'll have to manually get your bot token after a certain period, as that token expires within a couple hours._

For safety reasons, Twitch API (and many others) uses access tokens to check whether you're allowed to make an API call. Some technical stuff, but it basically means you need a "key" to be allowed to access certain "rooms". I compacted all the different URL's (which you can see in previous commits) into 1 big scope. This scope includes:

- Read chat
- Send messages in chat
- Read your mods list
- Manage your VIP list
- Create polls
- Listen for channel points redemptions

These last 2 will always be in the bot, but if you're not an Affiliate / Partner and tell the bot this when it starts up, it won't even do anything with these scopes.

You'll have to paste this URL in your **browser** and replace `<YOUR_CLIENT_ID>` with your actual application's Client ID.

```
https://id.twitch.tv/oauth2/authorize?client_id=<YOUR_CLIENT_ID>&redirect_uri=http://localhost&response_type=code&scope=chat:read+chat:edit+channel:manage:vips+channel:read:redemptions+channel:manage:polls+moderation:read+channel:manage:broadcast+moderator:read:followers
```

If you need to log in, do this. You will end up on your redirect link of your twitch application, but you only need the URL of this page. In the URL, you can find `code=<AUTHORIZATION_CODE>`. Copy this authorization code and place it in the `.env` file with the variable name "CODE".

With this code, you can get the access and refresh token that the bot will need. Run the script "GetAccessToken.exe" and you should see 2 new fields appearing in the `.env` file. Your command prompt may also flash and I know this is a sign of bad intentions, but I just haven't learned what to do with that part yet in college :/\
**IMPORTANT: DO NOT SHARE ANY OF THESE CODES WITH ANYONE**

When these tokens expire, the code should automatically trigger a token refresh and it should try to connect once more. If this is not the case, create an issue with the details of the error on the [GitHub page](https://github.com/CLFlix/KuroBot/issues) and I'll look into it. Manually restarting the bot should make it connect either way, though.

---

If you've completed the setup process, your `.env` file should look something like this (order doesn't matter):

```
TOKEN="YOUROAUTHTOKEN"
CHANNEL="Your-Twitch-Channel-Name"
osuUsername="Your-osu!-Username"
osuAuth="YOUROSUAPIKEY"

# General info
BROADCASTER_ID="broadcaster_id"
CLIENT_ID="YOUR-CLIENT-ID"
CLIENT_SECRET="YOUR-CLIENT-SECRET"

# Access Tokens
CODE="YOUR-AUTHORIZATION-CODE-FROM-MANUAL-URL"
ACCESS_TOKEN="YOUR-ACCESS-TOKEN"
REFRESH_TOKEN="YOUR-REFRESH-TOKEN"
```

## Commands

https://clflix.github.io/KuroBot/commands

## Redemptions

If enabled, this bot can listen to all redemptions made using Twitch channel points. With how it stands right now, the bot will only acknowledge rewards starting with "Exchange". This makes the bot retrieve the user that redeemed it and the cost of this reward, and add the cost to the user's bot <a href="#points">points</a>.\
Suggestions for different features are always welcome in https://github.com/CLFlix/KuroBot/discussions/categories/suggestions

## Title Updater

If enabled, the bot will perform a check every 10 minutes on your stream title, looking for a change in osu! rank. If there is a change in rank, the bot will then update your stream title with your current osu! rank, replacing your old rank. This will only work correctly if you have your osu! rank in the title between brackets: [\<rank>]. If you have multiple things between brackets in your title, let your rank be the first, since only the content of the first pair of brackets will be replaced.
