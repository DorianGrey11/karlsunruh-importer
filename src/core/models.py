from enum import Enum
from typing import Optional

from pydantic import BaseModel


class UserId(Enum):
    KOHI = "be9638f8-22f9-463a-b223-d1da83e2fa89"
    P8 = "9c9951f1-60c8-4e5c-9be9-fb7d0e59bf78"
    COLA_TAXI_OKAY = "134f4d14-86fb-4a27-9bc7-79ef9be58ec1"
    QUEERKASTLE = "c8853207-c310-46c2-a326-5b0b6b2fe8ef"
    KINEMATHEK = "bd4c503f-0554-4227-b7b2-a1817e02e0d9"
    CAFE_NOIR = "3c2e3bc9-6b84-424e-ac7d-7ccc23612647"
    WEICHE_KANTEN = "3f685bf5-0065-42da-badf-b211fbc504f5"
    KARLSUNRUH_IMPORTER = "574e37d0-381d-4629-96d2-af7ee19f330f"


class LocationId(Enum):
    KOHI = "id:a9d73764-caf4-406d-8ec9-63635ed3a707"
    P8 = "id:49dcab2a-afff-4c2e-a2f1-ab7f6bb6a099"
    COLA_TAXI_OKAY = "id:e3a6074e-14ea-4e3c-8416-252fd42a9ea4"
    QUEERKASTLE = "id:05f7d306-b6ed-4103-9a41-1f5802e2f653"
    KINEMATHEK = "id:db59cde2-d31a-46ae-a75f-6e1760e51847"
    CAFE_NOIR = "id:4884f7c4-0de4-45d2-bc9f-b703632a537e"


class GroupId(Enum):
    KOHI = "id:768040b3-7c05-4146-b11e-55229675d382"
    P8 = "id:50e0f008-9e08-4a1e-a8eb-3dc10cda360d"
    COLA_TAXI_OKAY = "id:0cbb44e8-6a62-4ada-8ca0-5a2780f66312"
    QUEERKASTLE = "id:c3b4dc8e-6350-43f8-b50f-75f82649f354"
    KINEMATHEK = "id:ad4dd0f6-313e-4a4c-ba3b-4a41c7fc473f"
    WEICHE_KANTEN = "id:d22cee7b-9173-4185-9d9e-8c8a7826780c"

class RepeatingEventId(Enum):
    TeamMeatCool = "revent:96631ac5-dc86-4aa7-9a6d-af3dc2e3b83d"
    OpenArtsClub = "revent:0a68c6b4-47f3-4907-9280-330426bd7650"
    PsstPlayClap = "revent:60bc0ed0-ff8f-418e-ae0b-3780b4b9271b"


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


class CreateEvent(BaseModel):
    address: Optional[str]
    category: Category | str
    description: str
    end: Optional[str]
    image: str | None # TODO check if this should be an empty string
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


class Event(CreateEvent):
    id: str


class Location(BaseModel):
    id: LocationId | str
    name: str
