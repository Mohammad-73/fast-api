from functools import lru_cache
from typing import Optional

from pydantic import Extra
from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    ENV_STATE: Optional[str] = None

    class Config:
        env_file: str = ".env"
        extra = Extra.ignore


class GlobalConfig(BaseConfig):
    DATABASE_URL: Optional[str] = None
    DB_FORCE_ROLL_BACK: bool = False
    DEV_MAILGUN_API_KEY: Optional[str] = None
    DEV_MAILGUN_DOMAIN: Optional[str] = None
    LOGTAIL_API_KEY: Optional[str] = None
    B2_KEY_ID: Optional[str] = None
    B2_APPLICATION_KEY: Optional[str] = None
    B2_BUCKET_NAME: Optional[str] = None


class DevConfig(GlobalConfig):
    class Config:
        env_prefix: str = "DEV_"


class ProdConfig(GlobalConfig):
    class Config:
        env_prefix: str = "PROD_"


class TestConfig(GlobalConfig):
    DATABASE_URL: str = "sqlite:///test.db"
    DB_FORCE_ROLL_BACK: bool = True

    class Config:
        env_prefix: str = "TEST_"


@lru_cache()
def get_config(env_state: Optional[str]):
    configs = {"dev": DevConfig, "test": TestConfig, "prod": ProdConfig}
    return configs[env_state or "dev"]()  # fallback if ENV_STATE is None


config = get_config(BaseConfig().ENV_STATE)
