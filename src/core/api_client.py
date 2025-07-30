import os
import json
import requests
from datetime import datetime
from typing import List, Optional

from src.core.config import API_URL, AUTH_EMAIL, AUTH_PASSWORD
from src.core.models import CreateEvent, Event, Location


def request_auth_token() -> str:
    res = requests.post(
        f"{API_URL}/auth/login",
        json={"email": AUTH_EMAIL, "password": AUTH_PASSWORD},
        timeout=10
    )
    res.raise_for_status()
    token = res.json().get("token")
    os.environ["API_TOKEN"] = token
    return token


def get_token() -> str:
    return f"{(os.getenv('API_TOKEN') or request_auth_token()).strip()}"


def fetch_events(
        start_after: Optional[datetime] = None,
        start_before: Optional[datetime] = None,
        deactivated: Optional[bool] = None,
        published: Optional[bool] = None,
        canceled: Optional[bool] = None,
) -> List[Event]:
    filters = {}

    def add_filter(key, value, transform=lambda x: x):
        if value is not None:
            filters[key] = transform(value)

    add_filter("startAfter", start_after, lambda dt: dt.isoformat(timespec='seconds') + "Z")
    add_filter("startBefore", start_before, lambda dt: dt.isoformat(timespec='seconds') + "Z")
    add_filter("deactivated", deactivated)
    add_filter("published", published)
    add_filter("canceled", canceled)

    res = requests.get(
        f"{API_URL}/events",
        params={
            "filters": json.dumps(filters)
        } if filters else None,
        timeout=10
    )
    res.raise_for_status()
    return [Event(**e) for e in res.json()]


def fetch_locations() -> List[Location]:
    res = requests.get(
        f"{API_URL}/places",
        timeout=10
    )
    res.raise_for_status()
    return [Location(**l) for l in res.json()]


def get_mime_type(extension: str) -> str:
    mime_types = {
        "jpg": "image/jpeg",
        "svg": "image/svg+xml",
        "tif": "image/tiff",
        "ico": "image/vnd.microsoft.icon",
    }
    return mime_types.get(extension.lower(), f"image/{extension.lower()}")


def send_image(url: str) -> str:
    res = requests.post(
        f"{API_URL}/media",
        files={'media': (url.split("/")[-1], requests.get(url).content, get_mime_type(url.split(".")[-1]))},
        headers={'Authorization': get_token()},
        timeout=10
    )
    return res.json().get("id", "")


def send_events(events: List[CreateEvent]) -> None:
    for event in events:
        if event.image:
            try:
                event.image = send_image(event.image)
            except:
                print(f"Failed to upload image for event '{event.name}', skipping image upload. Image: {event.image}")
                event.image = ""

        res = requests.post(
            f"{API_URL}/events",
            data=event.model_dump_json(),
            headers={
                "Authorization": get_token(),
                "Content-Type": "application/json"
            },
            timeout=10
        )
        res.raise_for_status()
        print(f"Event '{event.name}' created")
