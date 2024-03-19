import logging

from typing import Optional

import requests

from config import settings

from .base import TokenClientBase


_logger = logging.getLogger(__name__)


class UpstashTokenClient(TokenClientBase):

    _type = "upstash"

    @classmethod
    def store_token(cls, key: str, token: str) -> bool:
        try:
            res = requests.post(
                f"{settings.upstash_api_url}",
                data=f'["SET", "{key}", "{token}", "EX", "{settings.code_expire_seconds}"]',
                headers={
                    "Authorization": f"Bearer {settings.upstash_api_token}",
                    "Content-Type": "application/json",
                }
            ).json()
            if res.get("result") == "OK":
                return True
        except Exception as e:
            _logger.error(f"Store token failed: {e}")
        return False

    @classmethod
    def get_token(cls, key: str) -> Optional[str]:
        try:
            res = requests.post(
                f"{settings.upstash_api_url}",
                data=f'["GET", "{key}"]',
                headers={
                    "Authorization": f"Bearer {settings.upstash_api_token}",
                    "Content-Type": "application/json",
                }
            )
            if res.status_code != 200:
                _logger.error(f"Get token failed: {res.status_code} {res.text}")
                return None
            token = res.json().get("result")
            if not token:
                return None
            return token
        except Exception as e:
            _logger.error(f"Get token failed: {e}")
        return None
