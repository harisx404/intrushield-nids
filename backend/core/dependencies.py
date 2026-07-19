"""FastAPI dependency injection factories."""
from typing import Annotated
from fastapi import Depends, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.core.database import get_db
from backend.core.security import verify_token
from backend.core.exceptions import UnauthorizedException
from backend.repositories import user_repo
from backend.schemas.auth import UserResponse
from sqlalchemy.ext.asyncio import AsyncSession

_bearer = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserResponse:
    """Extract and validate the current authenticated user from JWT.
    
    Raises:
        HTTPException 401: If no token or token is invalid.
        HTTPException 401: If user no longer exists in database.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = verify_token(credentials.credentials)
        user_id: int = int(payload["sub"])
    except (UnauthorizedException, KeyError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    user = await user_repo.get(db, user_id)
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or deactivated",
        )
    return UserResponse.model_validate(user)


def require_role(*roles: str):
    """Factory for role-based access control dependency.
    
    Usage:
        @router.delete("/alerts/{id}", dependencies=[Depends(require_role("admin"))])
    """
    async def _check_role(
        current_user: Annotated[UserResponse, Depends(get_current_user)]
    ) -> UserResponse:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required role: {', '.join(roles)}. Your role: {current_user.role}",
            )
        return current_user
    return _check_role


# Shortcut dependencies
CurrentUser = Annotated[UserResponse, Depends(get_current_user)]
AdminRole = Depends(require_role("admin"))
AnalystRole = Depends(require_role("admin", "analyst"))

AdminOnly = Annotated[UserResponse, AdminRole]
AnalystPlus = Annotated[UserResponse, AnalystRole]
