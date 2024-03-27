import json
import logging
import secrets

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from config import settings
from models import User

from .base import DBClientBase
from fastapi import HTTPException


_logger = logging.getLogger(__name__)


class SqliteClient(DBClientBase):

    _type = "sqlite"

    sessionmaker = None

    @classmethod
    def init_db_client(cls):
        if cls.sessionmaker is None:
            engine = create_engine(settings.sqlite_db_url)
            tmp_sessionmaker = sessionmaker(bind=engine)
            # create table if not exists
            with tmp_sessionmaker() as session, open("db/sqlite3.sql") as f:
                for exec_sql in f.read().split(";"):
                    if exec_sql.strip():
                        session.execute(text(exec_sql))
            cls.sessionmaker = tmp_sessionmaker

    @classmethod
    def login_user(cls, user: User) -> bool:
        user_in_db = None
        try:
            cls.init_db_client()
            exex_sql = text(
                "SELECT * FROM awsl_users WHERE user_email = :user_email"
            )
            with cls.sessionmaker() as session:
                res = session.execute(
                    exex_sql.bind_arguments(user_email=user.user_email)
                )
                user_in_db = res.fetchone()
        except Exception as e:
            _logger.error(f"Failed to query user: {e}")
            raise HTTPException(
                status_code=400, detail=f"Failed to query user: {e}"
            )
        if not user_in_db:
            raise HTTPException(
                status_code=400, detail="User not found"
            )
        if not secrets.compare_digest(user_in_db.get("password", ""), user.password):
            raise HTTPException(
                status_code=400, detail="User password incorrect"
            )
        return True

    @classmethod
    def register_user(cls, user: User) -> bool:
        try:
            cls.init_db_client()
            exec_sql = text(
                "INSERT INTO awsl_users (user_name, user_email, password, updated_at)"
                " VALUES (:user_name, :user_email, :password, datetime('now'))"
                " ON CONFLICT (user_email) DO UPDATE"
                " SET user_name = :user_name, password = :password, updated_at = datetime('now')"
            )
            with cls.sessionmaker() as session:
                session.execute(exec_sql.bindparams(
                    user_name=user.user_name,
                    user_email=user.user_email,
                    password=user.password
                ))
                session.commit()
        except Exception as e:
            _logger.error(f"Failed to register user: {e}")
            raise HTTPException(
                status_code=400, detail=f"Failed to register user: {e}"
            )
        return True

    @classmethod
    def update_oauth_user(cls, user: User) -> bool:
        try:
            cls.init_db_client()
            exex_sql = text(
                "INSERT INTO awsl_oauth_users"
                " (login_type, user_name, user_email, web3_account, origin_data, updated_at)"
                " VALUES (:login_type, :user_name, :user_email, :web3_account, :origin_data, datetime('now'))"
                " ON CONFLICT (login_type, user_email) DO UPDATE"
                " SET user_name = :user_name, web3_account = :web3_account,"
                " origin_data = :origin_data, updated_at = datetime('now')"
            )
            with cls.sessionmaker() as session:
                session.execute(exex_sql.bindparams(
                    login_type=user.login_type,
                    user_name=user.user_name,
                    user_email=user.user_email,
                    web3_account=user.web3_account,
                    origin_data=json.dumps(user.origin_data)
                ))
                session.commit()
        except Exception as e:
            _logger.error(f"Failed to update user: {e}")
            raise HTTPException(
                status_code=400, detail=f"Failed to update user: {e}"
            )
        return True
