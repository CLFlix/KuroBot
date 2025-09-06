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
`osuAuth` is the authorization key you need for any request to the osu! API. You can find the details on how to get this on the bottom of your osu! account settings page.

The result should be something like this:

```
TOKEN="YOUROAUTHTOKEN"
CHANNEL="KurookamiTV"
osuUsername:"_Kurookami_"
osuAuth:"YOUROSUAPIKEY"
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

### ?points

Shows the player how many points this chatter has. Every chatter gains points through this little formula: `round(message_length / 4)`. There's also a cooldown of 5 seconds, so chatters aren't able to spam for points.

### ?leaderboard

Shows the top 3 point earners. Alias: `?lb`
