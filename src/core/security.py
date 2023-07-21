import datetime
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt
from .config import (
    ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)


def create_token(data: dict, refresh: bool = False) -> str:
    to_encode = data.copy()
    exp = REFRESH_TOKEN_EXPIRE_MINUTES if refresh else ACCESS_TOKEN_EXPIRE_MINUTES
    token_type = "ref" if refresh else "acc"
    to_encode.update(
        {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=exp),
            "type": token_type
        }
    )
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        encoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.JWTError:
        return None
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")
