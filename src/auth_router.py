import jwt
import uuid
import datetime
import logging

from fastapi import APIRouter, HTTPException

from config import settings
from models import OauthBody, TokenBody
from src.auth import AuthClientBase
from src.db.base import DBClientBase
from src.cache.base import TokenClientBase

router = APIRouter()
_logger = logging.getLogger(__name__)


@router.get("/api/login", tags=["Auth"])
def login(login_type: str, redirect_url: str = ""):
    client = AuthClientBase.get_client(login_type)
    return client.get_login_url(redirect_url)


@router.post("/api/oauth", tags=["Auth"])
def oauth(oauth_body: OauthBody):
    client = AuthClientBase.get_client(oauth_body.login_type)
    if oauth_body.app_id not in settings.app_settings:
        raise HTTPException(
            status_code=400, detail="App ID not found"
        )
    app_settings = settings.app_settings[oauth_body.app_id]
    try:
        user = client.get_user(oauth_body)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Can't get user info: {e}"
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
    token_client = TokenClientBase.get_client()
    code = uuid.uuid4().hex
    token_client.store_token(f"{app_settings.app_id}:{code}", jwt_value, settings.token_code_expire_seconds)
    # update user info to db if enabled
    if settings.enabled_db:
        db_client = DBClientBase.get_client()
        db_client.update_oauth_user(user)
    return {
        "redirect_url": app_settings.redirect_url,
        "code": code
    }


@router.post("/api/token", tags=["Auth"])
def token(token_body: TokenBody):
    token_client = TokenClientBase.get_client()
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
