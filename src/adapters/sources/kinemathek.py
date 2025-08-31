from typing import List
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from src.core.models import CreateEvent, Category, Topic, LocationId, UserId, GroupId
from src.adapters.sources.base import EventSource, DAYS_AHEAD_TO_REQUEST

KINEMATHEK_SPIELPLAN_API_URL = "https://kinemathek-karlsruhe.de/wp-json/wp/v2/pages/9808"

TAGS_TO_IMPORT = ["klima-krisen-utopien", "gemeinwohloekonomie"]


def map_event_tag_to_topic(event_tag: str) -> Topic:
    event_tag_mapping = {
        "klima-krisen-utopien": Topic.KLIMAGERECHTIGKEIT,
    }
    return event_tag_mapping.get(event_tag, Topic.SONSTIGES)


class KinemathekSource(EventSource):
    def get_events(self) -> List[CreateEvent]:
        try:
            response = requests.get(KINEMATHEK_SPIELPLAN_API_URL, timeout=10)
            response.raise_for_status()
            content = response.json().get("content").get("rendered")
            program_soup = BeautifulSoup(content, "html.parser")
        except:
            print("Failed to fetch events from Kinemathek.")
            return []

        events: List[CreateEvent] = []
        for wp_theatre_event in program_soup.find_all("div", class_="wp_theatre_event"):
            try:
                relevant_tag = next(
                    (tag for tag in TAGS_TO_IMPORT if wp_theatre_event.find("li", class_=f"wp_theatre_prod_tag_{tag}")),
                    None
                )
                if relevant_tag:
                    event_url = wp_theatre_event.find("a").get("href")
                    event_response = requests.get(event_url, timeout=10)
                    event_response.raise_for_status()
                    event_page_soup = BeautifulSoup(event_response.text, "html.parser")
                    event_soup = event_page_soup.find("div", id="filminhalt")
                    if event_soup is None:
                        continue

                    wp_theatre_event_datetimes = event_soup.find_all("div", class_="wp_theatre_event_datetime")
                    day, month, _ = wp_theatre_event_datetimes[1].get_text().split(".")
                    hour, minute = wp_theatre_event_datetimes[2].get_text().split(":")
                    year = datetime.now().year
                    if datetime.now().month - 4 > int(month):
                        year += 1
                    start = datetime(year, int(month), int(day), int(hour), int(minute),
                                     tzinfo=ZoneInfo("Europe/Berlin"))
                    if (start <= datetime.now(tz=start.tzinfo)
                            or start > datetime.now(tz=start.tzinfo) + timedelta(days=DAYS_AHEAD_TO_REQUEST)):
                        continue

                    description = "\n".join(
                        event_text.get_text() for event_text in
                        event_soup.find_all("p")[1:]) + f"\n\n{event_url}"

                    figure = event_soup.find("figure", class_="wp-block-image")
                    image = figure.find("img").get("src") \
                        if figure is not None \
                        else event_page_soup.find("meta", property="og:image").get("content")

                    events.append(
                        CreateEvent(
                            address='Kaiserpassage 6, 76133 Karlsruhe',
                            category=Category.FILM,
                            description=description,
                            end=(start + timedelta(hours=2)).isoformat(),
                            image=image,
                            involved=[],
                            lat=49.0106085,
                            lng=8.396970535,
                            location=LocationId.KINEMATHEK,
                            location2=None,
                            name=event_soup.find("div", class_="wp_theatre_prod_title").get_text(),
                            organizers=[GroupId.KINEMATHEK],
                            ownedBy=[UserId.KINEMATHEK, UserId.KARLSUNRUH_IMPORTER],
                            parent=None,
                            parentListed=False,
                            published=True,
                            start=start.isoformat(),
                            tags=[],
                            topic=map_event_tag_to_topic(relevant_tag),
                        )
                    )
            except Exception as e:
                print(f"Failed to fetch event from Kinemathek: {e}")
                continue
        return events


if __name__ == "__main__":  # FOR TESTING ONLY
    source = KinemathekSource()
    fetched_events = source.get_events()
    for event in fetched_events:
        print(event)
