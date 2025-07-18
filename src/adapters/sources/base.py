from abc import ABC, abstractmethod
from typing import List
from src.core.models import CreateEvent

DAYS_AHEAD_TO_REQUEST = 120


class EventSource(ABC):
    @abstractmethod
    def get_events(self) -> List[CreateEvent]:
        pass
