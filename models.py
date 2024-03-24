from typing import Optional
from pydantic import BaseModel, Field


class OauthBody(BaseModel):
    app_id: str
    login_type: str
    code: Optional[str] = None
    web3_account: Optional[str] = None
    redirect_url: Optional[str] = None


class TokenBody(BaseModel):
    app_id: str
    app_secret: str
    code: str


class EmailUser(BaseModel):
    email: str
    password: str = ""
    cf_token: str = ""
    code: str = ""


class User(BaseModel):
    login_type: str
    user_name: str
    user_email: str
    web3_account: Optional[str] = None
    origin_data: Optional[dict] = Field(None, exclude=True)
    password: Optional[str] = Field(None, exclude=True)
    expire_at: float = 0
