from backend.core.dependencies import CurrentUser, get_db
from backend.repositories.event_repository import event_repo
from backend.schemas.common import paginated
from backend.schemas.event import NetworkEventResponse
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("", summary="List all events")
async def read_events(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
) -> dict:
    """Retrieve raw network events."""
    skip = (page - 1) * per_page
    events, total = await event_repo.get_multi(db, skip=skip, limit=per_page)
    return paginated(
        data=[NetworkEventResponse.model_validate(e) for e in events],
        page=page,
        per_page=per_page,
        total=total,
        message="Events retrieved successfully",
    )
