### BROADCASTER_ID Token

```
curl -X POST "https://id.twitch.tv/oauth2/token" ^
     -H "Content-Type: application/x-www-form-urlencoded" ^
     -d "client_id=<YOUR_CLIENT_ID>" ^
     -d "client_secret=<YOUR_CLIENT_SECRET>" ^
     -d "grant_type=client_credentials"
```

Just copy this access token, you won't need this one further on.

### Actual BROADCASTER_ID request

```
curl -X GET https://api.twitch.tv/helix/users ^
     -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" ^
     -H "Client-Id: <YOUR_CLIENT_ID>"
```

Result: BROADCASTER_ID

### Access Token

```
https://id.twitch.tv/oauth2/authorize?client_id=<YOUR_CLIENT_ID>&redirect_uri=http://localhost&response_type=code&scope=chat:read+chat:edit+channel:manage:vips+channel:read:redemptions+channel:manage:polls+moderation:read
```

Result in ".env": CODE

### Result after execution of intial token script

```
TOKEN="Your-Twitch-OAuth-Token"
CHANNEL="Your-Channel-Name"
osuUsername:"Your-osu!-Username"
osuAuth:"Your-osu!-API-key"

# General info
BROADCASTER_ID="broadcaster_id"
CLIENT_ID="YOUR-CLIENT-ID"
CLIENT_SECRET="YOUR-CLIENT-SECRET"

# Access Tokens
CODE="YOUR-AUTHORIZATION-CODE-FROM-MANUAL-URL"
ACCESS_TOKEN="YOUR-ACCESS-TOKEN"
REFRESH_TOKEN="YOUR-REFRESH-TOKEN"
```
