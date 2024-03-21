import json
import logging
import secrets
import requests

from config import settings
from models import User

from .base import DBClientBase
from fastapi import HTTPException


_logger = logging.getLogger(__name__)


class SupabaseRestClient(DBClientBase):

    _type = "supabase_rest"

    @classmethod
    def login_user(cls, user: User) -> bool:
        res = requests.get(
            f"{settings.supabase_api_url}/rest/v1/awsl_users?user_email=eq.{user.user_email}",
            headers={
                "apikey": settings.supabase_api_key,
                "Authorization": f"Bearer {settings.supabase_api_key}",
            }
        )
        if res.status_code >= 400:
            _logger.error(f"Failed to login user: {res.status_code} {res.text}")
            raise HTTPException(
                status_code=400, detail="Failed to find user"
            )
        try:
            data = res.json()
        except Exception as e:
            _logger.error(f"Failed to parse user data: {e}")
            raise HTTPException(
                status_code=400, detail=f"Failed to parse user data: {e}"
            )
        if len(data) == 0:
            raise HTTPException(
                status_code=400, detail="User not found"
            )
        if not secrets.compare_digest(data[0].get("password", ""), user.password):
            raise HTTPException(
                status_code=400, detail="User password incorrect"
            )
        return True

    @classmethod
    def register_user(cls, user: User) -> bool:
        res = requests.post(
            f"{settings.supabase_api_url}/rest/v1/awsl_users?on_conflict=user_email",
            json={
                "user_name": user.user_name,
                "user_email": user.user_email,
                "password": user.password,
                "updated_at": "now()",
            },
            headers={
                "apikey": settings.supabase_api_key,
                "Authorization": f"Bearer {settings.supabase_api_key}",
                "Prefer": "resolution=merge-duplicates",
                "Content-Type": "application/json",
            }
        )
        if res.status_code >= 400:
            _logger.error(f"Failed to register user: {res.status_code} {res.text}")
            raise HTTPException(
                status_code=400, detail="Failed to register user"
            )
        return True

    @classmethod
    def update_oauth_user(cls, user: User) -> bool:
        res = requests.post(
            f"{settings.supabase_api_url}/rest/v1/awsl_oauth_users?on_conflict=login_type,user_email",
            json={
                "login_type": user.login_type,
                "user_name": user.user_name,
                "user_email": user.user_email,
                "web3_account": user.web3_account,
                "origin_data": json.dumps(user.origin_data),
                "updated_at": "now()",
            },
            headers={
                "apikey": settings.supabase_api_key,
                "Authorization": f"Bearer {settings.supabase_api_key}",
                "Prefer": "resolution=merge-duplicates",
                "Content-Type": "application/json",
            }
        )
        if res.status_code >= 400:
            _logger.error(f"Failed to update user: {res.status_code} {res.text}")
            raise HTTPException(
                status_code=400, detail="Failed to update user"
            )
        return True
