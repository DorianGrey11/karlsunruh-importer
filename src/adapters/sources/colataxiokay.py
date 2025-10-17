from datetime import datetime, timedelta
from typing import List
from zoneinfo import ZoneInfo

import requests
from src.core.models import CreateEvent, Category, Topic, LocationId, UserId, GroupId, RepeatingEventId
from src.adapters.sources.base import EventSource, DAYS_AHEAD_TO_REQUEST

COLA_TAXI_OKAY_URL = "https://cto.ekrem.space/api/events"

REPEATING_EVENTS = {
    "TEAM MEET COOL": RepeatingEventId.TeamMeatCool,
    "OPEN ARTS CLUB": RepeatingEventId.OpenArtsClub,
    "PSST PLAY CLAP": RepeatingEventId.PsstPlayClap
}


class ColaTaxiOkaySource(EventSource):
    def get_events(self) -> List[CreateEvent]:
        try:
            response = requests.get(COLA_TAXI_OKAY_URL, timeout=10)
            response.raise_for_status()
        except:
            print("Failed to fetch events from ColaTaxiOkay.")
            return []

        events: List[CreateEvent] = []
        for event in response.json()["events"]:
            if datetime.now().isoformat() < event['start'] < (
                    datetime.now() + timedelta(days=DAYS_AHEAD_TO_REQUEST)).isoformat():
                events.append(
                    CreateEvent(
                        address=None,
                        category=Category.SONSTIGES,
                        description=event['description'],
                        end=datetime.fromisoformat(event['end']).astimezone(ZoneInfo("Europe/Berlin")).isoformat(),
                        image=None,
                        involved=[],
                        lat=49.008172,
                        lng=8.4095862,
                        location=LocationId.COLA_TAXI_OKAY,
                        location2=None,
                        name=event['title'],
                        organizers=[GroupId.COLA_TAXI_OKAY],
                        ownedBy=[UserId.COLA_TAXI_OKAY, UserId.KARLSUNRUH_IMPORTER],
                        parent=REPEATING_EVENTS[event['title']] if event['title'] in REPEATING_EVENTS else None,
                        parentListed=False,
                        published=True,
                        start=datetime.fromisoformat(event['start']).astimezone(ZoneInfo("Europe/Berlin")).isoformat(),
                        tags=[],
                        topic=Topic.SONSTIGES,
                    )
                )
        return events


if __name__ == "__main__":  # FOR TESTING ONLY
    source = ColaTaxiOkaySource()
    fetched_events = source.get_events()
    for event in fetched_events:
        print(event)
