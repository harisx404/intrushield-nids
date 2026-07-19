"""Common Pydantic schemas shared across all API responses."""

from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginationMeta(BaseModel):
    """Pagination metadata included in list responses."""

    page: int
    per_page: int
    total: int
    total_pages: int


class ApiResponse(BaseModel, Generic[T]):
    """Standard API response envelope for all endpoints."""

    success: bool = True
    data: T | None = None
    message: str = "Success"
    meta: PaginationMeta | None = None


class ErrorResponse(BaseModel):
    """Standard error response returned by exception handlers."""

    success: bool = False
    error: str
    message: str
    detail: str | None = None
    request_id: str | None = None


def ok(data: T, message: str = "Success", meta: PaginationMeta | None = None) -> dict:
    """Helper to create a successful API response dict."""
    return ApiResponse(success=True, data=data, message=message, meta=meta).model_dump()


def paginated(
    data: list[T],
    page: int,
    per_page: int,
    total: int,
    message: str = "Retrieved successfully",
) -> dict:
    """Helper to create a paginated API response."""
    total_pages = max(1, -(-total // per_page))  # Ceiling division
    return ok(
        data=data,
        message=message,
        meta=PaginationMeta(
            page=page, per_page=per_page, total=total, total_pages=total_pages
        ),
    )
