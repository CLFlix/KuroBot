# KuroBot

## Installation

### For developers:

Before being able to run anything, you need to install some dependencies in order for the script to work. Open command prompt and navigate to this folder and run:

```
pip install -r requirements.txt
```

---

### All users:

You will need <a href="https://github.com/Piotrekol/StreamCompanion">StreamCompanion</a> in order for `?np` and `?nppp` to work. These features work by taking the data StreamCompanion processes and shows you on the locally hosted json.\
Also create a file called `points.json` in the same folder as the executable. This is were all the points of all the users will be stored. Simply open the file once and place `{}` inside it.

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

The bot will also need your broadcaster ID to be able to do some things on your channel, otherwise it doesn't know what channel to read your mods list (?polls), read your followers list (?followage),... You can run the "GetBroadcasterId.exe" for that, since it's fully automated now!

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

When these tokens expire, the code should automatically trigger a token refresh and it should try to connect once more. If this is not the case, create an issue with the details of the error on the github page and I'll look into it. Manually restarting the bot should make it connect either way, though.

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

## Redemptions

This bot also listens to all redemptions made using Twitch channel points. With how it stands right now, the bot will only acknowledge rewards starting with "Exchange". This makes the bot retrieve the user that redeemed it and the cost of this reward, and add the cost to the user's bot <a href="#points">points</a>.

## Useful Commands

<sup>I'll be working on a website to show all the commands in a better way, since this list system is not the best way...</sup>

### ?test

This just gives you a quick verification that the bot is ready to be used in your chat! It's recommended to run the bot before you start your stream, so you don't have to deal with this during stream.

### ?commands

This will show all the commands the viewers can use with your bot! `?commands` itself since you already know this command if you just triggered it. `test` will also be left out of this since viewers don't need to test the bot once you verified it's running in your chat.

### ?followage <@username>

By using `?followage`, you can see how long you've been following the streamer. If you want to see how long someone else has been following the streamer, you can use `?followage <@username>`.

### ?profile

Get the streamer's osu! profile link in the chat by using this command!

### ?np

`?np` is the well-known command where you can ask the bot what map the streamer is currently playing! Mods are also included. This will show you an output like this:

```
@kurookamitv Now playing: Yousei Teikoku - Ira [Wrath] https://osu.ppy.sh/b/4426662
```

### ?nppp

This will show the same thing as the command before this, including the pp amounts for SS, 99% and 95% FC.

```
@kurookamitv Now playing: Yousei Teikoku - Ira [Wrath] https://osu.ppy.sh/b/4426662 | PP: 95%: 453, 99%: 564, 100%: 615
```

### ?rank

This command will show you the rank of the account where `osuUsername` has been filled in.

```
@kurookamitv Global Rank: #8440, Country Rank: #47
```

### ?playtime

This will show you how much hours the streamer has wasted on this silly game.

### ?playcount

Similar to `?playtime`, the sent message coming from this command will contain the playcount of the streamer.

### ?osustats

Combining `?rank`, `?playtime` and `?playcount`, this command will tell you what rank the streamer is, how many pp they have, for how much hours they have played osu! and how many plays they have in the game. <sub>I might update this to be able to receive usernames and look up other users than the streamer</sub>

```
@kurookamitv _Kurookami_: #7394, Country rank: #44 - pp: 9807.84 - Playtime: 1610h - Playcount: 90863
```

### ?rq

This function responds dynamically to the streamer's choice! When you run the bot, you'll be greeted with this question:

```
Do you accept map requests this stream? (y/n)
```

When the command `?rq` get activated in the Twitch chat and you chose "y" in the question, the responding message will be: "You're free to request any map you'd like to see me play. Just paste the link in the chat!"
If you chose no, this will be: "I will not be accepting map requests this stream :/. Maybe next stream ;)"

### ?poll

With this command, you can start a poll that will run for 2 minutes. The command will have to be built like this:

```
?poll Is this a question? Yes No
```

The command will take everything until the '?' and take that as a question. Then it will look for all the spaces and make each word a choice of the poll. This means that you won't be able to use spaces in one choice. I'll be working on that soon. The choices of this poll would be: 1. Yes, 2. No. You can have a maximum number of 5 options in a poll.

## Fun commands

### ?stretch

If you think the streamer has been sitting still for a little while, enter `?stretch` in the chat to make them stretch or stand up for a bit. Helping that blood flow only has benefits ;)!

### ?posture

We all need to check our posture every now and then. To make the streamer do so, simply enter this command in the chat!

### ?hydrate

Talking with a dried up throat isn't gonna be very pleasant. Get the streamer to take a sip of their drink to rehydrate with this command!

### ?roll `number`

This will roll a randum number between 1 and `number` if it's specified like `?roll 1000`. If this is not specified, it will roll a random number between 1 and 100.

### ?owo `message`

After replacing all the l's and r's in the original `message`, the bot will reply with the same message in an owofied state.

```
Origial message: ?owo Hello, world!
Bot's reply: @KurookamiTV Hewwo, wowwd!
```

### ?mock `message`

When you use this command, the bot will return your message in SpOnGeBoB cApItAlIzAtIoN.

### ?rps `choice`

Play rock, paper, scissors with the bot! The player needs to type `?rps choice` in chat, with `choice` being one of the three choices: "rock", "paper" or "scissors". If the player wins, they get 3 points. If they lose, they get nothing (may be updated). If they tie, they get 1 point.

### ?claim

Users can claim 500 points upon first arrival in your chat! The username will be added to a file called `first_time_bonus_claimed.txt` and they won't be able to claim it again unless manually removed from the list.

### ?points

Shows the player how many points this chatter has. Every chatter gains points through this little formula: `round(message_length / 4)`. There's also a cooldown of 5 seconds, so chatters aren't able to spam for points.

### ?leaderboard

Shows the top 3 point earners. Alias: `?lb`

## Points redeeming

### ?bonk

Redeeming 2500 points, you can make the streamer shut up for 5 minutes! They don't necessarily have to mute their mic, but they just can't talk.

### ?memecam

This allows a chatter to redeem 500 points to make the streamer turn on a silly filter or modify their camera in any other meme-ish way for 10 minutes!

### ?invert

You can make the streamer turn their camera upside-down for 10 minutes by redeeming 250 points!

### ?zoom

Make the streamer absurdly zoom in their camera for the next 10 minutes with 500 points!

### ?endwith `map_link`

By redeeming 300 points, a chatter can trigger this command with the osu! beatmap's link of their choice. This map will be the one that has to be the last map of the stream / session.

### ?gift <@username> \<amount>

You can gift someone points by using this command! It sounds as easy as it is: by gifting some user some amount of points, this amount will be subtracted from your points and added to the receiver's amount of points.

### ?vip

Notifies the streamer that someone claimed the status of VIP for a limited amount of time and automatically tries to assign the VIP role to this user. The chatter will need 10.000 points for this.\
**This command will only work if the streamer did the complete setup, including the optional part for contacting the Twitch API.**
