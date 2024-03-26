from fastapi import HTTPException, status

from config import settings


class MetaMailClient(type):

    cilent_map = {}

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        if hasattr(cls, '_type'):
            MetaMailClient.cilent_map[cls._type] = cls


class MailClientBase(metaclass=MetaMailClient):

    @staticmethod
    def get_client() -> "MailClientBase":
        cls = MetaMailClient.cilent_map.get(settings.mail_client_type)
        if cls is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mail client type not supported"
            )
        return cls

    @classmethod
    def send_verify_code(cls, email: str, code: str) -> None:
        return
