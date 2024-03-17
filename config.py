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
    github_client_id: str = ""
    github_client_secret: str = Field(default="", exclude=True)
    app_settings: Dict[str, AppSettings] = Field(default={}, exclude=False)

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
