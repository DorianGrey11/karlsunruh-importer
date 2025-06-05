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


def fetch_events(start_after: Optional[datetime] = None, start_before: Optional[datetime] = None) -> List[Event]:
    params = {}
    filters = {}
    if start_after:
        filters["startAfter"] = start_after.isoformat(timespec='seconds') + "Z"
    if start_before:
        filters["startBefore"] = start_before.isoformat(timespec='seconds') + "Z"
    if filters:
        params["filters"] = json.dumps(filters)

    res = requests.get(
        f"{API_URL}/events",
        params=params,
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
            event.image = send_image(event.image)

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