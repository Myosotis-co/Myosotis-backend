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
from httpx_oauth.clients.linkedin import LinkedInOAuth2
from httpx_oauth.clients.reddit import RedditOAuth2

cookie_transport = CookieTransport(cookie_name="authCookie", cookie_max_age=3600)

SECRET = "verysecuresecretpisdec"


def get_jwt_strategy():
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


google_oauth_client = GoogleOAuth2("777490275004-dcuok40bfl21qpjg5a860ljoomrdtg68.apps.googleusercontent.com", "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")
github_oauth_client = GitHubOAuth2("ee229338dd853d5a0d5f", "c02ba600b6bba21567f809ac4365febe3fb4960a")

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user(active=True)
