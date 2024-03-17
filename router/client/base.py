from typing import Optional
from models import OauthBody, User


class MetaAuthClient(type):

    cilent_map = {}

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        if hasattr(cls, '_login_type'):
            MetaAuthClient.cilent_map[cls._login_type] = cls


class AuthClientBase(metaclass=MetaAuthClient):

    @staticmethod
    def get_client(login_type: str) -> Optional["AuthClientBase"]:
        cls = MetaAuthClient.cilent_map.get(login_type)
        if cls is None:
            return
        return cls

    @classmethod
    def get_login_url(cls) -> str:
        return None

    @classmethod
    def get_user(cls, oauth_body: OauthBody) -> Optional[User]:
        return None
