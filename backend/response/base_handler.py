from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseResponseHandler(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def should_handle(self, alert_data: Dict[str, Any]) -> bool:
        """Determine if this handler should process the alert."""
        pass

    @abstractmethod
    async def handle(self, alert_data: Dict[str, Any]) -> None:
        """Execute the response action."""
        pass
