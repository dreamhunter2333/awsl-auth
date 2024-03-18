import requests
import logging

from typing import Optional

from models import OauthBody, User

from router.client.base import AuthClientBase
from config import settings

_logger = logging.getLogger(__name__)


class Web3AuthClient(AuthClientBase):

    _login_type = "web3"

    @classmethod
    def get_login_url(cls, redirect_url: str = "") -> str:
        return ""

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
