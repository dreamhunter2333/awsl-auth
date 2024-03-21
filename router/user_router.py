import re
import uuid
import random
import string
import logging

from fastapi import APIRouter, HTTPException

from config import settings
from models import EmailUser, User
from router.auth.email import MailAuthClient
from router.db.base import DBClientBase
from router.email.base import MailClientBase
from router.token.base import TokenClientBase

router = APIRouter()
_logger = logging.getLogger(__name__)

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


@router.post("/api/email/login", tags=["Email"])
def login(email_user: EmailUser):
    token_client = TokenClientBase.get_client(settings.token_client)
    db_client = DBClientBase.get_client(settings.db_client)
    db_client.login_user(User(
        login_type=MailAuthClient._login_type,
        user_name=email_user.email,
        user_email=email_user.email,
        password=email_user.password,
    ))
    code = uuid.uuid4().hex
    token_client.store_token(f"email_login:{code}", email_user.email, settings.token_code_expire_seconds)
    return {
        "code": code
    }


@router.post("/api/email/verify_code", tags=["Email"])
def verify_code(email_user: EmailUser):
    if not EMAIL_REGEX.match(email_user.email):
        raise HTTPException(
            status_code=400, detail="Invalid email"
        )
    token_client = TokenClientBase.get_client(settings.token_client)
    mail_client = MailClientBase.get_client(settings.mail_client)
    token_client.check_rate_limit(
        "email_rate_limit", settings.email_rate_limit_timewindow_seconds,
        settings.email_rate_limit_max_requests
    )
    res = token_client.get_token(f"email_verify_code:{email_user.email}")
    if res:
        raise HTTPException(
            status_code=400, detail=f"Verify code already sent, Validity period {settings.verify_code_expire_seconds} seconds"
        )
    code = "".join(random.choices(string.digits, k=6))
    token_client.store_token(f"email_verify_code:{email_user.email}", code, settings.verify_code_expire_seconds)
    mail_client.send_verify_code(email_user.email, code)
    return {
        "timeout": settings.verify_code_expire_seconds,
    }


@router.post("/api/email/register", tags=["Email"])
def register(email_user: EmailUser):
    if not all([
            email_user.email,
            EMAIL_REGEX.match(email_user.email),
            email_user.password,
            email_user.code
    ]):
        raise HTTPException(
            status_code=400, detail="Invalid email user"
        )
    db_client = DBClientBase.get_client(settings.db_client)
    token_client = TokenClientBase.get_client(settings.token_client)
    res = token_client.get_token(f"email_verify_code:{email_user.email}")
    if not res:
        raise HTTPException(
            status_code=400, detail="Can't get verify code"
        )
    _logger.info(f"Verify code: {res}, input code: {email_user.code}")
    if res != email_user.code:
        raise HTTPException(
            status_code=400, detail="Verify code not match"
        )
    db_client.register_user(User(
        login_type=MailAuthClient._login_type,
        user_name=email_user.email,
        user_email=email_user.email,
        password=email_user.password,
    ))
    return {
        "status": "OK"
    }
