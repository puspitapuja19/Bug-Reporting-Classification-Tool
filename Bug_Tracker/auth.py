import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional

SECRET_KEY = "my_super_secret_key_12345"  # ⚠️ Move to .env in production
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token with expiration."""
    if expires_delta is None:
        expires_delta = timedelta(minutes=50)
    
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """Verify JWT token and return payload. Returns None if invalid."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.PyJWTError:
        return None  # Invalid token