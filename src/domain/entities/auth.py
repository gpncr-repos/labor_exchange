from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TokenEntity:
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


@dataclass
class TokenPayloadEntity:
    sub: str | None = None
    iat: datetime = field(default_factory=datetime.now)
