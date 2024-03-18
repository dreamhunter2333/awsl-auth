from typing import Optional
from pydantic import BaseModel


class OauthBody(BaseModel):
    app_id: str
    login_type: str
    code: Optional[str]
    redirect_url: Optional[str]


class User(BaseModel):
    login_type: str
    user_name: str
    user_email: str
    expire_at: float = 0
