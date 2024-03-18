import jwt
import datetime
import logging

from fastapi import APIRouter, HTTPException, status

from config import settings
from models import OauthBody
from router.client import AuthClientBase

router = APIRouter()
_logger = logging.getLogger(__name__)


@router.get("/api/settings", tags=["Auth"])
def auth_settings():
    return {
        "enabled_smtp": False,
        "enabled_github": bool(settings.github_client_id),
        "enabled_google": bool(settings.google_client_id),
    }


@router.get("/api/login", tags=["Auth"])
def login(login_type: str, redirect_url: str = ""):
    client = AuthClientBase.get_client(login_type)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Login type not supported"
        )
    return client.get_login_url(redirect_url)


@router.post("/api/oauth", tags=["Auth"])
def oauth(oauth_body: OauthBody):
    client = AuthClientBase.get_client(oauth_body.login_type)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Login type not supported"
        )
    if oauth_body.app_id not in settings.app_settings:
        raise HTTPException(
            status_code=400, detail="App ID not found"
        )
    app_settings = settings.app_settings[oauth_body.app_id]
    try:
        user = client.get_user(oauth_body)
    except Exception as e:
        _logger.error(f"Get user info failed: {e}")
        raise HTTPException(
            status_code=400, detail="Can't get user info"
        )
    if not user:
        raise HTTPException(
            status_code=400, detail="Can't get user info"
        )
    user.expire_at = (
        datetime.datetime.now() +
        datetime.timedelta(days=app_settings.token_expire_days)
    ).timestamp()
    jwt_value = jwt.encode(
        user.model_dump(),
        app_settings.app_secret,
        algorithm="HS256"
    )
    return {
        "redirect_url": app_settings.redirect_url,
        "jwt": jwt_value
    }
