"""Authentication routes — login and token issuance."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.dependencies import CurrentUser, get_db
from backend.repositories import audit_repo
from backend.schemas.auth import Token, UserResponse
from backend.services.auth_service import auth_service

router = APIRouter()


@router.post("/login", response_model=Token, summary="Authenticate and obtain an access token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Token:
    """OAuth2-compatible login. Accepts a username/password form and returns a JWT."""
    user = await auth_service.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Account is inactive"
        )

    await audit_repo.log_action(
        db, user_id=user.id, action="login", details="User successfully authenticated"
    )
    await db.commit()

    return Token(access_token=auth_service.issue_access_token(user), token_type="bearer")


@router.get("/me", response_model=UserResponse, summary="Get the current authenticated user")
async def read_current_user(current_user: CurrentUser) -> UserResponse:
    """Return the profile of the currently authenticated user."""
    return current_user
