from datetime import datetime, timedelta, timezone

from jose import jwt
import os

access_token_expiry = os.getenv("ACCESS_TOKEN_EXPIRE_DAY")
refresh_token_expiry = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")

jwt_secret_key = os.getenv('SECRET_KEY')
Algorithm = os.getenv('ALGORITHM')


def create_access_token(data: dict):
    # to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=int(access_token_expiry))
    # to_encode.update({"exp": expire})
    data.update({"exp": expire})
    encoded_jwt = jwt.encode(data, jwt_secret_key, algorithm=Algorithm)
    return encoded_jwt


def create_refresh_token(data: dict):
    expire = datetime.now(timezone.utc) + timedelta(days=int(refresh_token_expiry))
    data.update({"exp": expire})
    encoded_jwt = jwt.encode(data, jwt_secret_key, algorithm=Algorithm)
    return encoded_jwt


def verify_access_token(token: str):
    return jwt.decode(token, jwt_secret_key, algorithms=Algorithm)


def verify_refresh_token(token: str):
    return jwt.decode(token, jwt_secret_key, algorithms=Algorithm)
  

    

    