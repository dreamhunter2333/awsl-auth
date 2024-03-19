import requests
import logging

from typing import Optional

from models import OauthBody, User

from router.client.base import AuthClientBase
from config import settings

_logger = logging.getLogger(__name__)

MS_URL = f"https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize?" \
    f"client_id={settings.ms_client_id}" \
    "&response_type=code" \
    "&response_mode=query" \
    "&scope=https%3A%2F%2Fgraph.microsoft.com%2FUser.Read"
MS_TOEKN_URL = "https://login.microsoftonline.com/consumers/oauth2/v2.0/token"
MS_USER_URL = "https://graph.microsoft.com/v1.0/me"


class MsAuthClient(AuthClientBase):

    _login_type = "ms"

    @classmethod
    def get_login_url(cls, redirect_url: str = "") -> str:
        return f"{MS_URL}&redirect_uri={redirect_url}"

    @classmethod
    def get_user(cls, oauth_body: OauthBody) -> Optional[User]:
        if not oauth_body.code:
            return None
        token_res = requests.post(
            f"{MS_TOEKN_URL}",
            data={
                'client_id': settings.ms_client_id,
                'code': oauth_body.code,
                'redirect_uri': oauth_body.redirect_url,
                'grant_type': 'authorization_code',
                'client_secret': settings.ms_client_secret,
            },
            headers={"Accept": "application/json"}
        ).json()
        if not token_res.get('access_token'):
            raise ValueError("Can't get access token from microsoft")
        access_token = token_res['access_token']
        res = requests.get(
            MS_USER_URL,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json"
            }
        ).json()
        user_email = res.get('userPrincipalName')
        if not user_email:
            raise ValueError("Can't get user email from microsoft")
        user_name = user_email.replace("@outlook.com", "")
        return User(
            login_type=cls._login_type,
            user_name=user_name,
            user_email=user_email
        )
