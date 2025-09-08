# README

## Installation

Before being able to run anything, you need to install some dependencies in order for the script to work. Open command prompt and navigate to this folder and run:

```
pip install -r requirements.txt
```

You will also need <a href="https://github.com/Piotrekol/StreamCompanion">StreamCompanion</a> in order for `?np` and `?nppp` to work. These features work by taking the data StreamCompanion processes and shows you on the locally hosted json.

## Account and Authorization

You will need to fill in some fields in a `.env` file within this folder:

The `CHANNEL` field has to be filled with the channel you want the bot to chat in, if you use it normally, this will be your own channel name.\
`TOKEN` is one you can't show anyone, that's why the `.env` file is hidden here. You can easily find this token by going to Twitch on your browser and opening the `Network` tab in F12. Then you look for any `gql` entry and look for `Authorization` in the `Headers` section. The value will be `OAuth YOUROAUTHTOKEN`.\
`osuUsername` is self-explanatory.\
`osuAuth` is the authorization key you need for any request to the osu! API. You can find the details on how to get this on the bottom of your osu! account settings page.\
**The following are optional if you want to be able to assign VIP status through the bot. This won't work without these values.**\
First of all you'll need a **client ID** of a Twitch Application, so you can contact the twitch API.

1. Go to [Twitch Developer Console --> Applications](https://dev.twitch.tv/console/apps)
2. Log in
3. Register your bot. You can give it any name you want as long as it's valid. The redirect URL can be `http:localhost`. Category: Chat Bot
4. After creating, click on your freshly registered app and copy the client ID in the `.env` file with the variable name "CLIENT_ID".
5. You can also create a Client Secret which you'll also need. Create one and paste the secret in the `.env` file with the name "CLIENT_SECRET".

Your **broadcaster ID** is the ID you, the streamer, have on Twitch. You can quickly access it by throwing this is your terminal:

```
curl -H "Authorization: Bearer <YOUR_TOKEN>" \
     -H "Client-Id: <YOUR_CLIENT_ID>" \
     https://api.twitch.tv/helix/users
```

<sup>Replace \<YOUR_TOKEN> and \<YOUR_CLIENT_ID> with your actual data</sup>\
Then look for `"id":"123456789"`. This is your "BROADCASTER_ID" in your `.env`.

_Notice: The last thing you need can be done in 2 ways. I'm using the long-term setup, otherwise you'll have to manually get your bot token after a certain period, since that token expires within a couple hours._

The last thing you need is a **token with VIP scope**. For safety reasons, your Twitch Application also needs a valid token to contact the Twitch API. This setup will include a couple steps to automatically refresh the token using a code and a refresh token. The first step is retrieving the code by pasting this url in your browser:

```
https://id.twitch.tv/oauth2/authorize
  ?client_id=<YOUR_CLIENT_ID>
  &redirect_uri=http://localhost
  &response_type=code
  &scope=chat:read+chat:edit+channel:manage:vips
```

<sup>The only thing to replace here is \<YOUR_CLIENT_ID></sup>\
If you need to log in, do this. You will end up on your redirect link of your twitch application, but you only need the URL of this page. In the URL, you can find `code=<AUTHORIZATION_CODE>`. Copy this authorization code and place it in the `.env` file with the variable name "CODE".

Now you need to get your bot access token and refresh token, but don't worry, I handled that for you. Run "get_twitch_refresh_token.exe" and you should see 2 new fields appear in the `.env` file called "BOT_ACCESS_TOKEN" and "BOT_REFRESH_TOKEN". The access token expires within a couple hours, but I've also accounted to automatically refresh them when they do. You don't have to worry about these tokens in any way.

The result should be something like this:

```
TOKEN="YOUROAUTHTOKEN"
CHANNEL="KurookamiTV"
osuUsername:"_Kurookami_"
osuAuth:"YOUROSUAPIKEY"

# Optional:
BROADCASTER_ID=broadcaster_id
CLIENT_ID="YOUR-CLIENT-ID"
CLIENT_SECRET="YOUR-CLIENT-SECRET"
CODE="AUTHORIZATION_CODE"
BOT_ACCESS_TOKEN="BOT-ACCESS-TOKEN"
BOT_REFRESH_TOKEN="REFRESH-TOKEN"
```

## Useful Commands

### ?test

This just gives you a quick verification that the bot is ready to be used in your chat! It's recommended to run the bot before you start your stream, so you don't have to deal with this during stream.

### ?commands

This will show all the commands the viewers can use with your bot! `?commands` itself since you already know this command if you just triggered it. `test` will also be left out of this since viewers don't need to test the bot once you verified it's running in your chat.

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

This command will show you the rank of the account where `osuUsername` has been filled in. The output looks like this:

```
@kurookamitv Global Rank: #8440, Country Rank: #47
```

### ?playtime

This will show you how much hours the streamer has wasted on this silly game.

### ?playcount

Similar to `?playtime`, the sent message coming from this command will contain the playcount of the streamer.

### ?rq

This function responds dynamically to the streamer's choice! When you run the bot, you'll be greeted with this question:

```
Do you accept map requests this stream? (y/n)
```

When the command `?rq` get activated in the Twitch chat and you chose "y" in the question, the responding message will be: "You're free to request any map you'd like to see me play. Just paste the link in the chat!"
If you chose no, this will be: "I will not be accepting map requests this stream :/. Maybe next stream ;)"

## Fun commands

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

Users can claim 500 points upon first arrival in your chat! The username will be added to a file called `first_time_bonus_claimed.txt` and they won't be able to claim it again.

### ?points

Shows the player how many points this chatter has. Every chatter gains points through this little formula: `round(message_length / 4)`. There's also a cooldown of 5 seconds, so chatters aren't able to spam for points.

### ?leaderboard

Shows the top 3 point earners. Alias: `?lb`

## Points redeeming

### ?vip

Notifies the streamer that someone claimed the status of VIP for a limited amount of time and automatically tries to assign the VIP role to this user. The chatter will need {FILL IN POINTS AMOUNT} points for this.
