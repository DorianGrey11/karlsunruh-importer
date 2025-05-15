from enum import Enum
from typing import Optional

from pydantic import BaseModel


class UserId(Enum):
    KOHI = "be9638f8-22f9-463a-b223-d1da83e2fa89"
    KARLSUNRUH_IMPORTER = "574e37d0-381d-4629-96d2-af7ee19f330f"

class LocationId(Enum):
    KOHI = "id:a9d73764-caf4-406d-8ec9-63635ed3a707"

class GroupId(Enum):
    KOHI = "id:768040b3-7c05-4146-b11e-55229675d382"

class Category(Enum):
    BAR_CAFE = "2a531521-817a-4d3b-a853-ca4bc254b1c3"
    BERATUNG = "b67ac3fd-cf71-467c-814f-3d5588fb5a27"
    DIY = "67cb734c-442a-4fcf-9dc7-22dc0a8fcf26"
    DEMO_KUNDGEBUNG = "a844abaf-fc6b-4097-819e-a0d96e40875f"
    DISKUSSION = "98070939-a7ad-475d-a555-e5002504458f"
    FILM = "d5795597-271f-4ab1-afd2-ec8b01128517"
    KONZERT = "d5afeef9-1a5c-459c-bbf3-802a3ae8c5fc"
    PARTY = "a6ff52cd-d8a6-4679-bbaf-b8b068f01f88"
    SONSTIGES = "edabfcdc-b5bb-4f71-a26d-64339ebbe87c"
    TREFFEN = "716f6ac1-5754-49be-bf9d-3cb206e22488"
    VORTRAG = "d96685b7-5b01-49b6-a15c-b9e394a6ed5a"
    WORKSHOP = "e8d49f15-33ab-4a6b-9386-f17edbe22d9c"

class Topic(Enum):
    ANARCHISMUS = "e5cb34c9-9483-4c54-9960-2ed320b851fa"
    ANTIFASCHISMUS = "0ba014f5-3982-4e0e-aee9-41dcb720f520"
    ANTIRASSISMUS = "f106e2a8-7f33-46a1-86d4-ee59cc8591be"
    ANTISEMITISMUS = "9bf47f2b-b732-4456-b15b-a089768f3b64"
    ARBEITSKAMPF = "c505df1b-e07d-4abc-8f62-c57e41e7e5fe"
    DIY = "8c53b6b6-47a3-458d-9ea7-68be4ba35edd"
    INTERNATIONALISMUS = "1ffb2643-f483-40da-bdd9-c87fa782f925"
    KLIMAGERECHTIGKEIT = "5d756edc-e2d0-4242-bd71-590c969d804c"
    KULTUR = "9eef33d7-6244-4c71-8961-6c54526d35a9"
    MOBILITAET = "cad5594a-a9e8-4fbc-8cfd-75782853d060"
    QUEERFEMINISMUS = "c616cc5f-32bd-41fc-b90a-353de9e79733"
    REFUGEE_RIGHTS = "339d1d5b-17a9-4868-b5a2-c35a6a62b04d"
    REPRESSION = "3bccf0da-4c6d-47de-8668-1243c1973d3f"
    SOLIDARITAET = "b37939af-4c89-4b31-8fc2-8c0da5f2d948"
    SONSTIGES = "16b417bd-2e9a-469e-9fe9-81e296c5c8df"
    SOZIALISMUS = "cb90a4e1-4f71-40cd-9ca0-220d02911307"
    TIERRECHTE = "3071369a-7ad9-43be-a2ff-942c816c2a37"
    OEKOLOGIE = "93ecdc90-1099-4acb-bb34-e87912d71161"


class Event(BaseModel):
    address: str
    category: Category | str
    description: str
    end: Optional[str]
    image: str
    involved: list[dict]
    lat: float
    lng: float
    location: LocationId | str
    location2: Optional[str]
    name: str
    organizers: list[GroupId | str]
    ownedBy: list[UserId | str]
    parent: Optional[str]
    parentListed: bool
    published: bool
    start: str
    tags: list[str]
    topic: Topic | str