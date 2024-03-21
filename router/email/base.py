from fastapi import HTTPException, status


class MetaMailClient(type):

    cilent_map = {}

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        if hasattr(cls, '_type'):
            MetaMailClient.cilent_map[cls._type] = cls


class MailClientBase(metaclass=MetaMailClient):

    @staticmethod
    def get_client(client_type: str) -> "MailClientBase":
        cls = MetaMailClient.cilent_map.get(client_type)
        if cls is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mail client type not supported"
            )
        return cls

    @classmethod
    def send_verify_code(cls, email: str, code: str) -> None:
        return
