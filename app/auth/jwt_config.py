
from fastapi_users.authentication import CookieTransport,JWTStrategy

cookie_transport = CookieTransport(cookie_max_age=3600)

def get_jwt_strategy():
    return JWTStrategy(secret=SECRET_AUTH, lifetime_seconds=3600,tokenUrl="auth/jwt/login",cookie_transport=cookie_transport)