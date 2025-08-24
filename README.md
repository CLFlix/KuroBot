# README

## Installation

Before being able to run anything, you need to install some dependencies in order for the script to work. Open command prompt and navigate to this folder and run:

```
pip install -r requirements.txt
```

You will also need <a href="https://github.com/Piotrekol/StreamCompanion">StreamCompanion</a> in order for `!np` to work. The function uses a file that's part of StreamCompanion.

## Account and Authorization

You will need to fill in some fields in a `.env` file within this folder:

The `CHANNEL` field has to be filled with the channel you want the bot to chat in, if you use it normally, this will be your own channel name.\
`TOKEN` is one you can't show anyone, that's why the `.env` file is hidden here. You can easily find this token by going to Twitch on your browser and opening the `Network` tab in F12. Then you look for any `gql` entry and look for `Authorization` in the `Headers` section. The value will be `OAuth YOUROAUTHTOKEN`.\
`osuUsername` is self-explanatory.\
`osuAuth` is the authorization key you need for any request to the osu! API. You can find the details on how to get this on the bottom of your osu! account settings page.

The result should be something like this:

```
TOKEN="YOUROAUTHTOKEN"
CHANNEL="KurookamiTV"
osuUsername:"_Kurookami_"
osuAuth:"YOUROSUAPIKEY"
```

## Commands

### !cmds

The same as the classic "!commands" command, but purposely called `!cmds` to not trigger Nightbot or any other bots' "!commands" command. This will send a message in chat with a simple listing of all the commands available. If the amount of commands get too much for this, I'll try to find another way to make this a useful command without it being too cluttered.

### !np

`!np` is the well-known command where you can ask the bot what map the streamer is currently playing! Mods are also included. This will show you an output like this:

```
@kurookamitv Now playing: Yousei Teikoku - Ira [Wrath] https://osu.ppy.sh/b/4426662
```

### !nppp

This will show the same thing as the command before this, including the pp amounts for SS, 99% and 95% FC.

```
@kurookamitv Now playing: Yousei Teikoku - Ira [Wrath] https://osu.ppy.sh/b/4426662 | PP: 95%: 453, 99%: 564, 100%: 615
```

### !rank

This command will show you the rank of the account where `osuUsername` has been filled in. The output looks like this:

```
@kurookamitv Global Rank: #8440, Country Rank: #47
```

### !playtime

This will show you how much hours the streamer has wasted on this silly game.

### !playcount

Similar to `!playtime`, the sent message coming from this command will contain the playcount of the streamer.

### !rq

This function responds dynamically to the streamer's choice! When you run the bot, you'll be greeted with this question:

```
Do you accept map requests this stream? (y/n)
```

When the command `!rq` get activated in the Twitch chat and you chose "y" in the question, the responding message will be: "You're free to request any map you'd like to see me play. Just paste the link in the chat!"
If you chose no, this will be: "I will not be accepting map requests this stream :/. Maybe next stream ;)"
