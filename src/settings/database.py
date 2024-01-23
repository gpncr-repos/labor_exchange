from pydantic import BaseSettings, Field


class DataBaseSettings(BaseSettings):
    # дефолтные значения для кредов указываю в рамках допущения, что это тестовая задача)
    # в идеале их не должно быть в коде ни в каком виде
    user: str = Field(env="DB_USER", default="admin")
    password: str = Field(env="DB_PASS", default="admin")
    host: str = Field(env="DB_HOST", default="localhost")
    name: str = Field(env="DB_NAME", default="labor-exchange")
    port: int = Field(env="DB_PORT", default=8503)
    echo: bool = Field(env="DB_ECHO", default=False)
