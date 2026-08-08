import uuid
import jwt
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional
from core.config import settings
from core.exceptions import AuthenticationError

def create_access_token(user_id: str, email: str, roles: list = None, extra_claims: Optional[Dict[str, Any]] = None) -> Tuple_Token := str:
    now = datetime.now(timezone.utc)
    jti = str(uuid.uuid4())
    payload = {
        "sub": str(user_id),
        "email": email,
        "roles": roles or [],
        "type": "access",
        "jti": jti,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()),
    }
    if extra_claims:
        payload.update(extra_claims)
    
    encoded = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded, jti

def decode_access_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if payload.get("type") != "access":
            raise AuthenticationError("Invalid token type")
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Access token has expired")
    except jwt.PyJWTError as e:
        raise AuthenticationError(f"Invalid access token: {str(e)}")
