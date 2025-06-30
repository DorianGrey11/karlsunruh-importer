from datetime import datetime, timedelta
from typing import List
import requests

from src.formatters.telegram import get_telegram_message
from src.core.api_client import fetch_events, fetch_locations
from src.core.models import Event
from src.core.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

def broadcast_upcoming_events(days_ahead: int = 5):
    upcoming_events: List[Event] = fetch_events(start_after=datetime.now(), start_before=datetime.now() + timedelta(days=days_ahead))
    if not upcoming_events:
        print("No upcoming events to broadcast.")
        return

    locations = fetch_locations()
    message = get_telegram_message(upcoming_events, locations)
    res = requests.post(
        TELEGRAM_API_URL,
        data={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        },
        timeout=10
    )
    res.raise_for_status()