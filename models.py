from typing import Optional
from pydantic import BaseModel


class OauthBody(BaseModel):
    app_id: str
    login_type: str
    code: Optional[str] = None
    web3_account: Optional[str] = None
    redirect_url: Optional[str] = None


class User(BaseModel):
    login_type: str
    user_name: str
    user_email: str
    web3_account: Optional[str] = None
    expire_at: float = 0
