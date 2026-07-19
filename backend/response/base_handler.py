"""Abstract base class for all NIDS response handlers."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from backend.schemas.alert import AlertResponse


@dataclass
class ResponseResult:
    """Result of a single response handler execution."""
    handler_name: str
    action: str
    status: str           # "SUCCESS" | "FAILED" | "SKIPPED"
    details: dict[str, Any]


class BaseResponseHandler(ABC):
    """Abstract response handler — inherit to add new response types."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique name for this handler (used in logs and DB records)."""
        ...

    def should_handle(self, alert: AlertResponse) -> bool:
        """Determine if this handler should process the given alert.
        
        Override in subclasses to implement severity thresholds.
        Default: handle all alerts.
        """
        return True

    @abstractmethod
    async def handle(self, alert: AlertResponse) -> ResponseResult:
        """Execute the response action for the given alert.
        
        Must never raise exceptions — return ResponseResult with status="FAILED"
        and log the error internally instead.
        """
        ...
