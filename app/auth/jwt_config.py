from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    CookieTransport,
    JWTStrategy,
    AuthenticationBackend,
)

from app.auth.manager import get_user_manager
from app.auth.models import User

from httpx_oauth.clients.google import GoogleOAuth2
from httpx_oauth.clients.github import GitHubOAuth2

cookie_transport = CookieTransport(
    cookie_name="authCookie", cookie_max_age=3600, cookie_secure=False
)

# Secret used for encryption. Should be very secure.
SECRET = "verysecuresecretpisdec"


# Gives a json web token, an online signature used for authentication.
def get_jwt_strategy():
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


# To Get Client ID and Secret you need to visit the respective provider and register your app.
# Used for auhtentication through 3rd party apps and receiving an access token.
# Warning!: Keep ID and SECRET very secure. Should be encrypted into the future.
google_oauth_client = GoogleOAuth2("777490275004-dcuok40bfl21qpjg5a860ljoomrdtg68.apps.googleusercontent.com", "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")
github_oauth_client = GitHubOAuth2("Ov23liC72QTqp6ep9qIi", "ba1b482fe289b74f9288e81d6e6e9da68a40086b")


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user(active=True)
