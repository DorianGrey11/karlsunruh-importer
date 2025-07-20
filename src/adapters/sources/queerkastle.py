import html
from datetime import datetime, timedelta
from typing import List
from zoneinfo import ZoneInfo

import requests
from src.core.models import CreateEvent, Category, Topic, LocationId, UserId, GroupId
from src.adapters.sources.base import EventSource, DAYS_AHEAD_TO_REQUEST

QUEERKASTLE_URL = "https://queerkastle.de/wp-json/tribe/events/v1/events/"
QUEERKASTLE_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class QueerKAstleSource(EventSource):
    def get_events(self) -> List[CreateEvent]:
        try:
            response = requests.get(
                QUEERKASTLE_URL,
                params={
                    "starts_after": datetime.now().date().isoformat(),
                    "starts_before": (datetime.now() + timedelta(days=DAYS_AHEAD_TO_REQUEST)).date().isoformat(),
                    "status": "publish",
                    "per_page": 50,
                },
                timeout=10)
            response.raise_for_status()
        except:
            print("Failed to fetch events from QueerKAstle.")
            return []

        events: List[CreateEvent] = []
        for event in response.json()["events"]:
            start = datetime.strptime(event["start_date"], QUEERKASTLE_DATE_FORMAT).replace(
                tzinfo=ZoneInfo(event["timezone"]))
            end = datetime.strptime(event["end_date"], QUEERKASTLE_DATE_FORMAT).replace(
                tzinfo=ZoneInfo(event["timezone"])) \
                if event["end_date"] else start + timedelta(hours=2)
            events.append(
                CreateEvent(
                    address=f"{event['venue']['address']}, {event['venue']['zip']} {event['venue']['city']}",
                    category=Category.SONSTIGES,
                    description=html.unescape(event['description']) + "\n" + event['url'],
                    end=end.isoformat(),
                    image=event['image']['url'] if event['image'] else None,
                    involved=[],
                    lat=49.0041532 if event["venue"]["venue"] == "Queeres Zentrum Karlsruhe" else 0,
                    lng=8.37001 if event["venue"]["venue"] == "Queeres Zentrum Karlsruhe" else 0,
                    location=LocationId.QUEERKASTLE if event["venue"]["venue"] == "Queeres Zentrum Karlsruhe"
                    else event["venue"]["venue"],
                    location2=None,
                    name=html.unescape(event['title']),
                    organizers=[GroupId.QUEERKASTLE],
                    ownedBy=[UserId.QUEERKASTLE, UserId.KARLSUNRUH_IMPORTER],
                    parent=None,
                    parentListed=False,
                    published=True,
                    start=start.isoformat(),
                    tags=[],
                    topic=Topic.QUEERFEMINISMUS,
                )
            )
        return events


if __name__ == "__main__":  # FOR TESTING ONLY
    source = QueerKAstleSource()
    fetched_events = source.get_events()
    for event in fetched_events:
        print(event)
