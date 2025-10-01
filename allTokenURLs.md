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

### VIP Code

```
https://id.twitch.tv/oauth2/authorize
  ?client_id=<YOUR_CLIENT_ID>
  &redirect_uri=http://localhost
  &response_type=code
  &scope=chat:read+chat:edit+channel:manage:vips
```

Result: CODE_VIP

### Redemptions Code

```
https://id.twitch.tv/oauth2/authorize
  ?client_id=<YOUR_CLIENT_ID>
  &redirect_uri=http://localhost
  &response_type=code
  &scope=channel:read:redemptions
```

Result: CODE_REDEMPTIONS

### Polls Code

```
https://id.twitch.tv/oauth2/authorize
  ?client_id=<YOUR_CLIENT_ID>
  &redirect_uri=http://localhost
  &response_type=code
  &scope=channel:manage:polls
```

Result: CODE_POLLS

### Result after execution of intial token scripts

```
TOKEN="YOUROAUTHTOKEN"
CHANNEL="KurookamiTV"
osuUsername:"_Kurookami_"
osuAuth:"YOUROSUAPIKEY"

# Optional:
# General info
BROADCASTER_ID=broadcaster_id
CLIENT_ID="YOUR-CLIENT-ID"
CLIENT_SECRET="YOUR-CLIENT-SECRET"

# VIP Tokens
CODE_VIP="AUTHORIZATION_CODE"
ACCESS_TOKEN_VIP="ACCESS_TOKEN_WITH_SCOPE_VIP"
REFRESH_TOKEN_VIP="REFRESH_TOKEN_WITH_SCOPE_VIP"

# Redemptions Tokens
CODE_REDEMPTIONS="AUTHORIZATION_CODE_WITH_SCOPE_REDEMPTIONS"
ACCESS_TOKEN_REDEMPTIONS="ACCESS_TOKEN_WITH_SCOPE_REDEMPTIONS"
REFRESH_TOKEN_REDEMPTIONS="REFRESH_TOKEN_WITH_SCOPE_REDEMPTIONS"

# Polls Tokens
CODE_POLLS="AUTHORIZATION_CODE_WITH_SCOPE_POLLS"
ACCESS_TOKEN_POLLS="ACCESS_TOKEN_WITH_SCOPE_POLLS"
REFRESH_TOKEN_POLLS="REFRESH_TOKEN_WITH_SCOPE_POLLS"
```
