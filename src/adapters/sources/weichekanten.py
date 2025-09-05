from datetime import datetime, timedelta
from typing import List
from zoneinfo import ZoneInfo

import requests
from src.core.models import CreateEvent, Category, Topic, LocationId, UserId, GroupId
from src.adapters.sources.base import EventSource, DAYS_AHEAD_TO_REQUEST

WEICHEKANTEN_URL = "https://queerka.de/api/events/within"
WEICHEKANTEN_ORGA_ID = "66905827fdc9b53dcb468cb0"


class WeicheKantenSource(EventSource):
    def get_events(self) -> List[CreateEvent]:
        try:
            response = requests.get(
                WEICHEKANTEN_URL,
                params={
                    "startDateTime": datetime.now().date().isoformat(),
                    "endDateTime": (datetime.now() + timedelta(days=DAYS_AHEAD_TO_REQUEST)).date().isoformat(),
                    "orgId": WEICHEKANTEN_ORGA_ID
                },
                timeout=10)
            response.raise_for_status()
        except:
            print("Failed to fetch events from Weiche Kanten.")
            return []

        events: List[CreateEvent] = []
        for event in response.json():
            if event["Title"].replace(" ", "").lower() == "weichekantenplenum":
                continue

            start = datetime.fromisoformat(event["startDateTime"]).astimezone(ZoneInfo("Europe/Berlin"))
            end = datetime.fromisoformat(event["endDateTime"]).astimezone(ZoneInfo("Europe/Berlin")) \
                if event["endDateTime"] else start + timedelta(hours=2)

            if event["Location"].replace(" ", "").lower() in {"cafénoir", "cafenoir"}:
                location = LocationId.CAFE_NOIR
                lat = 48.9886097
                lon = 8.37200907
                owned_by = [UserId.WEICHE_KANTEN, UserId.CAFE_NOIR, UserId.KARLSUNRUH_IMPORTER]
            else:
                location = event["Location"]
                lat = 0
                lon = 0
                owned_by = [UserId.WEICHE_KANTEN, UserId.KARLSUNRUH_IMPORTER]

            events.append(
                CreateEvent(
                    address=event['Address'],
                    category=Category.SONSTIGES,
                    description=event['Description'],
                    end=end.isoformat(),
                    image=f"https://queerka.de/imageupload/eventImages/{event['imgPrefix']}{event['Images'][0]['name']}" \
                        if len(event['Images']) > 0 else None,
                    involved=[],
                    lat=lat,
                    lng=lon,
                    location=location,
                    location2=None,
                    name=event['Title'],
                    organizers=[GroupId.WEICHE_KANTEN],
                    ownedBy=owned_by,
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
    source = WeicheKantenSource()
    fetched_events = source.get_events()
    for event in fetched_events:
        print(event)
