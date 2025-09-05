import pkgutil
import importlib
import inspect
from datetime import datetime
from typing import List, Set, Tuple
from src.core.api_client import fetch_events, send_events
from src.core.models import CreateEvent, Event
from src.adapters.sources.base import EventSource
import src.adapters.sources as sources


def discover_sources() -> List[EventSource]:
    sources_found = []
    for _, module_name, _ in pkgutil.iter_modules(sources.__path__):  # uses the actual package path
        module = importlib.import_module(f"src.adapters.sources.{module_name}")
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, EventSource) and obj is not EventSource:
                sources_found.append(obj())
    return sources_found

def event_key(e) -> Tuple[str, float]:
    return e.name.strip(), datetime.fromisoformat(e.start).timestamp()

def dedupe(scraped: List[CreateEvent], existing: List[Event]) -> List[CreateEvent]:
    existing_keys: Set[Tuple[str, float]] = {event_key(e) for e in existing}
    return [e for e in scraped if event_key(e) not in existing_keys]


def run_sync():
    all_events: List[CreateEvent] = []
    for source in discover_sources():
        try:
            events = source.get_events()
            all_events.extend(events)
        except Exception as e:
            print(f"Failed to fetch from {source.__class__.__name__}: {e}")

    existing = fetch_events(start_after=datetime.now())
    new_events = dedupe(all_events, existing)

    if new_events:
        send_events(new_events)
    print(f"Inserted {len(new_events)} new events.")
