from authlib.integrations.starlette_client import OAuth
from fastapi_users.authentication import BearerTransport, AuthenticationBackend, JWTStrategy

from app.core.config import settings


oauth = OAuth()

oauth.register(
    name="google",
    client_id=settings.client_id,
    client_secret=settings.client_secret,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

bearer_transport = BearerTransport(tokenUrl="auth/google/callback")

jwt_strategy = JWTStrategy(secret=settings.secret, lifetime_seconds=3600)

google_oauth_backend = AuthenticationBackend(
    name="google",
    transport=bearer_transport,
    get_strategy=lambda: jwt_strategy,
)
