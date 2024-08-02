import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent
ENV_FILE = os.path.join(BASE_DIR, ".env")


class CustomSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


class DbSettings(CustomSettings):
    echo: bool = False
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int

    @property
    def db_url(self):
        return (f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@"
                f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}")


class AuthJWT(CustomSettings):
    jwt_secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 300
    refresh_token_expire_days: int = 3
    token_type_field_name: str = "token_type"
    access_token_name: str = "access"
    refresh_token_name: str = "refresh"


class Settings(CustomSettings):
    db: DbSettings = DbSettings()
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
