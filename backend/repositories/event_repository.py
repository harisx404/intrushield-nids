from backend.models.event import NetworkEvent
from backend.repositories.base import BaseRepository
from backend.schemas.event import NetworkEventCreate


class EventRepository(
    BaseRepository[NetworkEvent, NetworkEventCreate, NetworkEventCreate]
):
    pass


event_repo = EventRepository(NetworkEvent)
