import json
from typing import List

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from src.core.models import CreateEvent, Category, Topic, LocationId, UserId, GroupId
from src.adapters.sources.base import EventSource, DAYS_AHEAD_TO_REQUEST

KOHI_URL = "https://kohi.de/"


def map_event_type_to_category(event_type: str) -> Category:
    event_type_mapping = {
        "Literatur": Category.SONSTIGES,
        "Konzert": Category.KONZERT,
        "Theater": Category.SONSTIGES,
        "Querfunk": Category.KONZERT,
        "Songslam": Category.KONZERT,
        "Open Mic": Category.SONSTIGES
    }
    return event_type_mapping.get(event_type, Category.SONSTIGES)


class KohiSource(EventSource):
    def get_events(self) -> List[CreateEvent]:
        try:
            response = requests.get(KOHI_URL, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
        except:
            print("Failed to fetch events from KOHI.")
            return []

        events: List[CreateEvent] = []
        for script_tag in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script_tag.string)
                if not isinstance(data, dict) or data.get("@type") != "Event":
                    continue

                start = datetime.fromisoformat(data["startDate"])
                if (start <= datetime.now(tz=start.tzinfo)
                        or start > datetime.now(tz=start.tzinfo) + timedelta(days=DAYS_AHEAD_TO_REQUEST)):
                    continue

                event_infos = script_tag.find_previous("article").select_one(".eventInfos")
                full_description = event_infos.get_text(separator="\n", strip=True) if event_infos \
                    else data["description"]
                event_header = script_tag.find_previous("article").select_one(".flexbox__headline")
                name = event_header.find("h2").contents[0] if event_infos \
                    else data["name"].split("//")[0].strip()

                events.append(
                    CreateEvent(
                        address=f'{data["location"]["address"]["streetAddress"]}, {data["location"]["address"]["postalCode"]} {data["location"]["address"]["addressLocality"]}',
                        category=map_event_type_to_category(data["eventType"]),
                        description=full_description,
                        end=(start + timedelta(hours=2)).isoformat(),
                        image=data["image"],
                        involved=[],
                        lat=49.0016763,
                        lng=8.407540161512713,
                        location=LocationId.KOHI,
                        location2=None,
                        name=name,
                        organizers=[GroupId.KOHI],
                        ownedBy=[UserId.KOHI, UserId.KARLSUNRUH_IMPORTER],
                        parent=None,
                        parentListed=False,
                        published=True,
                        start=start.isoformat(),
                        tags=[],  # [tag.strip() for tag in data["genre"].split("/") if tag.strip() != ""],
                        topic=Topic.KULTUR,
                    )
                )
            except Exception:
                continue
        return events


if __name__ == "__main__":  # FOR TESTING ONLY
    source = KohiSource()
    fetched_events = source.get_events()
    for event in fetched_events:
        print(event)
