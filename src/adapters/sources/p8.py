from typing import List

import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from src.core.models import CreateEvent, Category, Topic, LocationId, UserId, GroupId
from src.adapters.sources.base import EventSource

P8_API_URL = "https://backend.p-acht.org/api/graphql"


def to_unicode_bold(text: str) -> str:
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    bold = (
        "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭"
        "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇"
    )
    return text.translate(str.maketrans(normal, bold))


def richtext_to_unicode_text(document):
    lines = []
    for block in document:
        if block["type"] == "paragraph":
            paragraph = ""
            for child in block.get("children", []):
                text = child.get("text", "")
                if child.get("bold"):
                    text = to_unicode_bold(text)
                paragraph += text
            lines.append(paragraph)
    return "\n".join(lines)


class P8Source(EventSource):
    def get_events(self) -> List[CreateEvent]:
        query = """
        query Events($from: DateTime!, $to: DateTime!) {
          events(where: { dateFrom: { gte: $from, lte: $to } }) {
            id
            name
            dateFrom
            dateTo
            location {
                street
                zipcode
                city
                }
            description {
                document
                }
            image {
              url
            }
          }
        }
        """
        variables = {
            "from": datetime.now().isoformat() + "Z",
            "to": (datetime.now() + timedelta(days=120)).isoformat() + "Z"
        }
        try:
            response = requests.post(
                P8_API_URL,
                json={"query": query, "variables": variables},
            )
        except:
            print("Failed to fetch events from P8.")
            return []

        events = []
        for event in response.json()["data"]["events"]:
            start = datetime.fromisoformat(event["dateFrom"]).astimezone(ZoneInfo("Europe/Berlin"))
            end = datetime.fromisoformat(event["dateTo"]).astimezone(ZoneInfo("Europe/Berlin")) \
                if event["dateTo"] else start + timedelta(hours=2)
            events.append(
                CreateEvent(
                    address=f'{event["location"]["street"]}, {event["location"]["zipcode"]} {event["location"]["city"]}',
                    category=Category.KONZERT,
                    description=richtext_to_unicode_text(event["description"]["document"]),
                    end=end.isoformat(),
                    image="https://backend.p-acht.org" + event["image"]["url"] if event["image"] else None,
                    involved=[],
                    lat=49.0016763,
                    lng=8.407540161512713,
                    location=LocationId.P8,
                    location2=None,
                    name=event["name"],
                    organizers=[GroupId.P8],
                    ownedBy=[UserId.P8, UserId.KARLSUNRUH_IMPORTER],
                    parent=None,
                    parentListed=False,
                    published=True,
                    start=start.isoformat(),
                    tags=[],
                    topic=Topic.KULTUR,
                )
            )
        return events


if __name__ == "__main__":  # FOR TESTING ONLY
    source = P8Source()
    fetched_events = source.get_events()
    for event in fetched_events:
        print(event)
