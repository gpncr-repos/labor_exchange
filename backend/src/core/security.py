import datetime
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from jose import jwt
from .config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)


# def refresh_access_token(token: str) -> str:
#     decoded_token = decode_access_token(token)
#     if decoded_token is None:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid auth token")
#
#     user_data = decoded_token.get("sub")
#
#     to_encode = {}
#
#     new_token = create_access_token({"sub": user_data}, to_encode)  # Передаем пустой словарь to_encode
#
#     return new_token


def create_access_token(data: dict, to_encode: dict = None) -> str:
    if to_encode is None:
        to_encode = data.copy()
    else:
        to_encode.update(data)
    to_encode.update({"exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    try:
        encoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.JWSError:
        return None
    return encoded_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super(JWTBearer, self).__call__(request)
        exp = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid auth token")
        if credentials:
            token = decode_access_token(credentials.credentials)
            if token is None:
                raise exp
            return credentials.credentials
        else:
            raise exp
