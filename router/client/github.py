import requests
import logging

from typing import Optional

from models import OauthBody, User

from router.client.base import AuthClientBase
from config import settings

_logger = logging.getLogger(__name__)

GITHUB_URL = "https://github.com/login/oauth/authorize?" \
    f"client_id={settings.github_client_id}"
GITHUB_TOEKN_URL = "https://github.com/login/oauth/access_token" \
    f"?client_id={settings.github_client_id}" \
    f"&client_secret={settings.github_client_secret}"
GITHUB_USER_URL = "https://api.github.com/user"


class GithubAuthClient(AuthClientBase):

    _login_type = "github"

    @classmethod
    def get_login_url(cls, redirect_url: str = "") -> str:
        return GITHUB_URL

    @classmethod
    def get_user(cls, oauth_body: OauthBody) -> Optional[User]:
        if not oauth_body.code:
            return None
        token_res = requests.post(
            f"{GITHUB_TOEKN_URL}&code={oauth_body.code}",
            headers={"Accept": "application/json"}
        ).json()
        access_token = token_res['access_token']
        res = requests.get(
            GITHUB_USER_URL,
            headers={
                "Authorization": f"token {access_token}",
                "Accept": "application/json"
            }
        ).json()
        user_name = res['login']
        user_email = res['email']
        return User(
            login_type=cls._login_type,
            user_name=user_name,
            user_email=user_email
        )
