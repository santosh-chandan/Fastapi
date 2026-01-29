# app/core/security.py
from fastapi import HTTPException, status
from passlib.context import CryptContext
from datetime import timedelta, datetime
from jose import jwt, JWTError, ExpiredSignatureError

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
SECRET_KEY = "super-secret"
ALGORITHM = "HS256"

# Token lifetimes
ACCESS_TOKEN_MINUTES = 15
REFRESH_TOKEN_DAYS = 7

def hash_password(password: str) -> str:
    if password.startswith("$argon2"):
        raise ValueError("Password already hashed")
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

# Creates a JWT token with expiration INSIDE the token.
def create_token(data: dict, expres_delta: timedelta, token_type: str) -> str:
    payload = data.copy
    payload['exp'] = datetime.utcnow() + expres_delta
    payload['type'] = token_type

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# Decodes JWT
def decode_token(data: str) -> dict:
    """
    Decodes JWT and automatically checks:
    - signature
    - expiration (exp)
    """
    try:
        return jwt.decode(data, SECRET_KEY, algorithms=ALGORITHM)
    
    # Token expired → exp claim failed
    except ExpiredSignatureError:
        return HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    
    # Invalid token / signature
    except JWTError:
        return HTTPException(
            status_code=401,
            detail="Invalid Token"
        )
