import logging

from typing import Optional

from models import OauthBody, User

from src.auth.base import AuthClientBase

_logger = logging.getLogger(__name__)


class Web3AuthClient(AuthClientBase):

    _login_type = "web3"

    @classmethod
    def get_user(cls, oauth_body: OauthBody) -> Optional[User]:
        if not oauth_body.web3_account:
            return None
        return User(
            login_type=cls._login_type,
            user_name=oauth_body.web3_account,
            user_email=oauth_body.web3_account,
            web3_account=oauth_body.web3_account
        )
