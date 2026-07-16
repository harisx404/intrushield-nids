from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.dependencies import get_db
from backend.services.auth_service import auth_service, create_access_token
from backend.schemas.auth import Token

router = APIRouter()

@router.post("/login/access-token", response_model=Token)
async def login_access_token(
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """OAuth2 compatible token login, get an access token for future requests."""
    user = await auth_service.authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
        
    # Create audit log
    from backend.repositories import audit_repo
    await audit_repo.log_action(db, user_id=user.id, action="login", details="User successfully authenticated")
    await db.commit()
        
    return {
        "access_token": create_access_token(user.id),
        "token_type": "bearer",
    }
