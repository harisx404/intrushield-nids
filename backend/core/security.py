"""JWT token creation and verification for NIDS authentication."""
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from backend.core.config import settings
from backend.core.exceptions import UnauthorizedException

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def get_password_hash(password: str) -> str:
    """Hash a plaintext password using bcrypt with work factor 12."""
    return _pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a bcrypt hash.
    
    Uses constant-time comparison to prevent timing attacks.
    """
    return _pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict[str, Any]) -> str:
    """Create a JWT access token with 60-minute expiry."""
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload.update({"exp": expire, "type": ACCESS_TOKEN_TYPE})
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(data: dict[str, Any]) -> str:
    """Create a JWT refresh token with 7-day expiry."""
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
    )
    payload.update({"exp": expire, "type": REFRESH_TOKEN_TYPE})
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def verify_token(token: str, expected_type: str = ACCESS_TOKEN_TYPE) -> dict[str, Any]:
    """Decode and verify a JWT token.
    
    Args:
        token: JWT string to verify.
        expected_type: Token type claim to validate ("access" or "refresh").
        
    Returns:
        Decoded token payload dict.
        
    Raises:
        UnauthorizedException: If token is invalid, expired, or wrong type.
    """
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        if payload.get("type") != expected_type:
            raise UnauthorizedException("Invalid token type")
        return payload
    except JWTError as exc:
        raise UnauthorizedException("Token is invalid or expired") from exc
