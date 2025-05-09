import os
from typing import List
import requests
from datetime import datetime

from core.config import API_URL, AUTH_EMAIL, AUTH_PASSWORD
from src.core.models import Event


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


def fetch_existing_events() -> List[Event]:
    res = requests.get(f'{API_URL}/events?filters={{"startAfter":"{datetime.now().isoformat()[:-7]}Z"}}')
    res.raise_for_status()
    return [Event(**e) for e in res.json()]


def send_image(url: str) -> str:
    res = requests.post(
        f"{API_URL}/media",
        files={'media': (url.split("/")[-1], requests.get(url).content, 'image/webp')},
        headers={'Authorization': get_token()},
        timeout=10
    )
    return res.json().get("id", "")


def send_events(events: List[Event]) -> None:
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
