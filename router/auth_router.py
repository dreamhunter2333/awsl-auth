import jwt
import uuid
import datetime
import logging

from fastapi import APIRouter, HTTPException, status

from config import settings
from models import OauthBody, TokenBody
from router.client import AuthClientBase
from router.token.base import TokenClientBase

router = APIRouter()
_logger = logging.getLogger(__name__)


@router.get("/api/settings", tags=["Auth"])
def auth_settings():
    return {
        "enabled_smtp": False,
        "enabled_github": bool(settings.github_client_id),
        "enabled_google": bool(settings.google_client_id),
        "enabled_ms": bool(settings.ms_client_id),
        "enabled_web3": settings.enabled_web3_client,
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
            detail="Login type not supported"
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
    token_client = TokenClientBase.get_client(settings.token_client)
    if not token_client:
        raise HTTPException(
            status_code=400, detail="Token client not found"
        )
    code = uuid.uuid4().hex
    res = token_client.store_token(f"{app_settings.app_id}:{code}", jwt_value)
    if not res:
        raise HTTPException(
            status_code=400, detail="Store token failed"
        )
    return {
        "redirect_url": app_settings.redirect_url,
        "code": code
    }


@router.post("/api/token", tags=["Auth"])
def token(token_body: TokenBody):
    token_client = TokenClientBase.get_client(settings.token_client)
    if not token_client:
        raise HTTPException(
            status_code=400, detail="Token client not found"
        )
    jwt_value = token_client.get_token(f"{token_body.app_id}:{token_body.code}")
    if not jwt_value:
        raise HTTPException(
            status_code=400, detail="Token not found or expired"
        )
    return {
        "jwt": jwt_value
    }
