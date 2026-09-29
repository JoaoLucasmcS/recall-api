import os
from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

Environment = Literal["dev", "prod"]


def _resolve_env_file():
    env = os.getenv("ENVIRONMENT", "dev")
    if env not in {"dev", "prod"}:
        raise ValueError(f"ENVIRONMENT inválido {env}, tente 'dev' ou 'prod'")

    return f".env.{env}"


class Settings(BaseSettings):
    environment: Environment = "dev"

    url_dDragon_campeoes: str

    frontend_url: str

    model_config = SettingsConfigDict(
        env_file=_resolve_env_file(),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def is_dev(self) -> bool:
        return self.environment == "dev"

    @property
    def is_prod(self) -> bool:
        return self.environment == "prod"


@lru_cache
def get_settings():
    return Settings()
