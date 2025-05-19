from abc import ABC, abstractmethod
from typing import List
from src.core.models import CreateEvent

class EventSource(ABC):
    @abstractmethod
    def get_events(self) -> List[CreateEvent]:
        pass