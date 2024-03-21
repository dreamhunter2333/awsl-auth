from fastapi import HTTPException, status

from models import User
from config import settings


class MetaDBClient(type):

    cilent_map = {}

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        if hasattr(cls, '_type'):
            MetaDBClient.cilent_map[cls._type] = cls


class DBClientBase(metaclass=MetaDBClient):

    @staticmethod
    def get_client(db_type: str) -> "DBClientBase":
        if not settings.enabled_db:
            raise HTTPException(
                status_code=400, detail="DB not enabled"
            )
        cls = MetaDBClient.cilent_map.get(db_type)
        if cls is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="DB type not supported"
            )
        return cls

    @classmethod
    def login_user(cls, user: User) -> bool:
        return True

    @classmethod
    def register_user(cls, user: User) -> bool:
        return True

    @classmethod
    def update_oauth_user(cls, user: User) -> bool:
        return True
