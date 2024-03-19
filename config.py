import logging
from typing import Dict

from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings

logging.basicConfig(
    format="%(asctime)s: %(levelname)s: %(name)s: %(message)s",
    level=logging.INFO
)
_logger = logging.getLogger(__name__)


class AppSettings(BaseModel):
    app_id: str
    app_secret: str
    redirect_url: str
    token_expire_days: int = 30


class Settings(BaseSettings):
    token_client: str = "upstash"
    redis_url: str = Field(default="", exclude=True)
    upstash_api_url: str = ""
    upstash_api_token: str = Field(default="", exclude=True)
    code_expire_seconds: int = 30
    google_client_id: str = ""
    google_client_secret: str = Field(default="", exclude=True)
    github_client_id: str = ""
    github_client_secret: str = Field(default="", exclude=True)
    enabled_web3_client: bool = True
    app_settings: Dict[str, AppSettings] = Field(default={}, exclude=True)

    @field_validator('app_settings')
    def convert_app_settings(cls, values: Dict[str, AppSettings]):
        return {
            app_settings.app_id: app_settings
            for _, app_settings in values.items()
        }

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"


settings = Settings()
_logger.info(f"settings: {settings.model_dump_json(indent=2)}")
