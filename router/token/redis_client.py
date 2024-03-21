from fastapi import HTTPException
import redis
import logging

from typing import Optional

from config import settings

from .base import TokenClientBase


_logger = logging.getLogger(__name__)


class RedisTokenClient(TokenClientBase):

    _type = "redis"
    redis_client = None

    @classmethod
    def init_redis(cls):
        if cls.redis_client is None:
            cls.redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)

    @classmethod
    def store_token(cls, key: str, token: str, expire_seconds: int) -> None:
        cls.init_redis()
        try:
            cls.redis_client.set(key, token, ex=expire_seconds)
            return
        except Exception as e:
            _logger.error(f"Store token failed: {e}")
        raise HTTPException(
            status_code=400, detail="Store token failed"
        )

    @classmethod
    def get_token(cls, key: str) -> Optional[str]:
        cls.init_redis()
        try:
            return cls.redis_client.get(key)
        except Exception as e:
            _logger.error(f"Get token failed: {e}")
            return None

    @classmethod
    def check_rate_limit(cls, key: str, time_window_seconds: int, max_requests: int) -> None:
        return
