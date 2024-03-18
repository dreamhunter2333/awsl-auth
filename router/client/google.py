import requests
import logging

from typing import Optional

from models import OauthBody, User

from router.client.base import AuthClientBase
from config import settings

_logger = logging.getLogger(__name__)

GOOGLE_URL = "https://accounts.google.com/o/oauth2/v2/auth?" \
    "response_type=code" \
    "&scope=https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile" \
    f"&client_id={settings.google_client_id}"
GOOGLE_TOEKN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USER_URL = "https://www.googleapis.com/oauth2/v1/userinfo"


class GoogleAuthClient(AuthClientBase):

    _login_type = "google"

    @classmethod
    def get_login_url(cls, redirect_url: str = "") -> str:
        return f"{GOOGLE_URL}&redirect_uri={redirect_url}"

    @classmethod
    def get_user(cls, oauth_body: OauthBody) -> Optional[User]:
        if not oauth_body.code:
            return None
        token_res = requests.post(
            f"{GOOGLE_TOEKN_URL}?code={oauth_body.code}",
            data={
                'code': oauth_body.code,
                'client_id': settings.google_client_id,
                'redirect_uri': oauth_body.redirect_url,
                'client_secret': settings.google_client_secret,
                'grant_type': 'authorization_code'
            },
            headers={"Accept": "application/json"}
        ).json()
        access_token = token_res['access_token']
        res = requests.get(
            GOOGLE_USER_URL,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json"
            }
        ).json()
        user_email = res.get('email')
        if not user_email:
            raise ValueError("Can't get user email from google")
        user_name = user_email.replace("@gmail.com", "")
        return User(
            login_type=cls._login_type,
            user_name=user_name,
            user_email=user_email
        )
