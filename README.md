# README

## Installation

If you haven't installed twitchio and / or dotenv yet, this won't work. You will have to run this into your command prompt in order to make this work on your PC:

```
pip install "twitchio<3"
pip install python-dotenv
```

## Account and Authorization

You will need to fill in 3 fields in a `.env` within this folder:

`BOT_NICK` will be the username the bot has to use to chat. If you want to let it go through your own account; just fill in your own username.\
The `CHANNEL` field has to be filled with the channel you want the bot to chat in, if you use it normally, this will be your own channel name.\
`TOKEN` is one you can't show anyone, that's why the `.env` file is hidden here. You can easily find this token by going to Twitch on your browser and opening the `Network` tab in F12. Then you look for any `gql` entry and look for `Authorization` in the `Headers` section. The value will be OAuth YOUROAUTHTOKEN.

The result should be something like this:

```
TOKEN="YOUROAUTHTOKEN"
BOT_NICK="KurookamiTV"
CHANNEL="KurookamiTV"
```
