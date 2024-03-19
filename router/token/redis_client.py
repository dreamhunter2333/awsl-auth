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
    def store_token(cls, key: str, token: str) -> bool:
        cls.init_redis()
        try:
            cls.redis_client.set(key, token, ex=settings.code_expire_seconds)
            return True
        except Exception as e:
            _logger.error(f"Store token failed: {e}")
        return False

    @classmethod
    def get_token(cls, key: str) -> Optional[str]:
        cls.init_redis()
        try:
            return cls.redis_client.get(key)
        except Exception as e:
            _logger.error(f"Get token failed: {e}")
            return None
