from typing import Optional

from fastapi import HTTPException, status

from config import settings


class MetaTokenClient(type):

    cilent_map = {}

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        if hasattr(cls, '_type'):
            MetaTokenClient.cilent_map[cls._type] = cls


class TokenClientBase(metaclass=MetaTokenClient):

    @staticmethod
    def get_client() -> "TokenClientBase":
        cls = MetaTokenClient.cilent_map.get(settings.cache_client_type)
        if cls is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token client type not supported"
            )
        return cls

    @classmethod
    def store_token(cls, key: str, token: str, expire_seconds: int) -> None:
        return

    @classmethod
    def get_token(cls, key: str) -> Optional[str]:
        return None

    @classmethod
    def check_rate_limit(cls, key: str, time_window_seconds: int, max_requests: int) -> None:
        return
