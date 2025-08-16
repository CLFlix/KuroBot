# README

## Installation

If you haven't installed twitchio and / or dotenv yet, this won't work. You will have to run this into your command prompt in order to make this work on your PC:

```
pip install "twitchio<3"
pip install python-dotenv
```

You will also need <a href="https://github.com/Piotrekol/StreamCompanion">StreamCompanion</a> in order for `!np` to work. The function uses a file that's part of StreamCompanion.

## Account and Authorization

You will need to fill in some fields in a `.env` file within this folder:

`BOT_NICK` will be the username the bot has to use to chat. If you want to let it go through your own account; just fill in your own username.\
The `CHANNEL` field has to be filled with the channel you want the bot to chat in, if you use it normally, this will be your own channel name.\
`TOKEN` is one you can't show anyone, that's why the `.env` file is hidden here. You can easily find this token by going to Twitch on your browser and opening the `Network` tab in F12. Then you look for any `gql` entry and look for `Authorization` in the `Headers` section. The value will be `OAuth YOUROAUTHTOKEN`.\
`osuUsername` is self-explanatory.\
`osuAuth` is the authorization key you need for any request to the osu! API. You can find the details on how to get this on the bottom of your osu! account settings page.

The result should be something like this:

```
TOKEN="YOUROAUTHTOKEN"
BOT_NICK="KurookamiTV"
CHANNEL="KurookamiTV"
osuUsername:"_Kurookami_"
osuAuth:"YOUROSUAPIKEY"
```

## Commands

### !np

`!np` is the well-known command where you can ask the bot what map the streamer is currently playing! This will show you an output like this:

```
@kurookamitv Now playing: Poppy - they're all around us [Coward] CS:4.5 AR:9.8 OD:9 HP:8.5
```

### !rank

This command will show you the rank of the account where `osuUsername` has been filled in. The output looks like this:

```
@kurookamitv Global Rank: #8440, Country Rank: #47
```
