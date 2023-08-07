from httpx_oauth.integrations.fastapi import OAuth2AuthorizeCallback
from httpx_oauth.oauth2 import OAuth2

client = OAuth2("CLIENT_ID", "CLIENT_SECRET", "AUTHORIZE_ENDPOINT", "ACCESS_TOKEN_ENDPOINT")
oauth2_authorize_callback = OAuth2AuthorizeCallback(client, "oauth-callback")
app = FastAPI()

@app.get("/oauth-callback", name="oauth-callback")
async def oauth_callback(access_token_state=Depends(oauth2_authorize_callback)):
    token, state = access_token_state