from pydantic_settings import BaseSettings


class AuthSettings(BaseSettings):
    access_token_expire_minutes: int = 60
    algorithm: str = "HS256"
    secret_key: str = "kNV6B5OQRML0ATHK1GfOpV5HwZ5l9Vwi"
