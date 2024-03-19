from typing import Optional


class MetaTokenClient(type):

    cilent_map = {}

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        if hasattr(cls, '_type'):
            MetaTokenClient.cilent_map[cls._type] = cls


class TokenClientBase(metaclass=MetaTokenClient):

    @staticmethod
    def get_client(login_type: str) -> Optional["TokenClientBase"]:
        cls = MetaTokenClient.cilent_map.get(login_type)
        if cls is None:
            return
        return cls

    @classmethod
    def store_token(cls, key: str, token: str) -> bool:
        return False

    @classmethod
    def get_token(cls, key: str) -> Optional[str]:
        return None
