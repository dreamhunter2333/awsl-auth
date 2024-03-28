import logging

from typing import Optional

from models import OauthBody, User

from src.auth.base import AuthClientBase
from src.cache import TokenClientBase

_logger = logging.getLogger(__name__)


class MailAuthClient(AuthClientBase):

    _login_type = "email"

    @classmethod
    def get_user(cls, oauth_body: OauthBody) -> Optional[User]:
        if not oauth_body.code:
            return None
        token_client = TokenClientBase.get_client()
        user_email = token_client.get_token(f"email_login:{oauth_body.code}")
        if not user_email:
            raise ValueError("Can't get user email from token")
        return User(
            login_type=cls._login_type,
            user_name=user_email,
            user_email=user_email,
        )
