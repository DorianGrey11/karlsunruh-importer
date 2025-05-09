from abc import ABC, abstractmethod
from typing import List
from src.core.models import Event

class EventSource(ABC):
    @abstractmethod
    def get_events(self) -> List[Event]:
        pass