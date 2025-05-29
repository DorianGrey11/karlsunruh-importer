from collections import defaultdict
from datetime import datetime
from typing import List
import locale

from src.core.config import BASE_URL
from src.core.models import Event, LocationId, Location

locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")

clocks = {
    0: "🕛", 1: "🕐", 2: "🕑", 3: "🕒", 4: "🕓", 5: "🕔", 6: "🕕", 7: "🕖", 8: "🕗", 9: "🕘", 10: "🕙", 11: "🕚",
    12: "🕛", 13: "🕐", 14: "🕑", 15: "🕒", 16: "🕓", 17: "🕔", 18: "🕕", 19: "🕖", 20: "🕗", 21: "🕘", 22: "🕙", 23: "🕚"
}


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
    for event in sorted(events, key=lambda e: e.start):
        day = datetime.fromisoformat(event.start).strftime("%A, %d. %B %Y")
        grouped[day].append(event)

    lines = []
    days = list(grouped.keys())
    for day in days:
        lines.append(f"*📅  {day}  📅*")
        for event in grouped[day]:
            start = datetime.fromisoformat(event.start)
            lines.append(
                f"{clocks[start.hour]}{start.strftime('%H:%M Uhr')}"
                f"  [{event.name}]({BASE_URL}event/{event.id}?ref=telegram-broadcast)"
                f"  📍{format_location(event.location, locations)}"
            )
        lines.append("\n")

    message = (f"  _{days[0]} - {days[-1]}_ \n\n"
               f"📣 *Veranstaltungen in* [KarlsUNRUH]({BASE_URL}?ref=telegram-broadcast) 📣 \n\n\n")
    message += "\n".join(lines)
    return message
