from collections import defaultdict
from datetime import datetime
from typing import List
import locale

from src.core.config import BASE_URL
from src.core.models import Event, LocationId, Location

locale.setlocale(locale.LC_TIME, "de_DE")


def format_location(location: LocationId | str, locations: List[Location]):
    if location.startswith("id:"):
        found_locations = [l for l in locations if l.id == location[3:]]
        if found_locations:
            found_location = found_locations[0]
            name = found_location.name
            return f"[{name}]({BASE_URL}ort/{found_location.id}?ref=telegram-broadcast)"
    return location


def get_telegram_message(events: List[Event], locations) -> str:
    grouped = defaultdict(list)
    for event in events:
        day = datetime.fromisoformat(event.start).strftime("%A, %d %b %Y")
        grouped[day].append(event)

    lines = []
    days = sorted(grouped.keys(), key= lambda x: datetime.strptime(x,"%A, %d %b %Y"))
    for day in days:
        lines.append(f"*📅 {day} 📅*")
        for event in grouped[day]:
            lines.append(
                f"🕒{datetime.fromisoformat(event.start).strftime('%H:%M Uhr')}"
                f"  [{event.name}]({BASE_URL}event/{event.id}?ref=telegram-broadcast)"
                f"  📍{format_location(event.location, locations)}"
                f"\n"
            )

    message = (f"  _{days[0]} - {days[-1]}_ \n\n"
               f"📣 *Veranstaltungen in* [Karlsunruh]({BASE_URL}?ref=telegram-broadcast) 📣 \n\n")
    message += "\n".join(lines)
    return message
