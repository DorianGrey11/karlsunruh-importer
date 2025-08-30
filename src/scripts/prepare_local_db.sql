INSERT INTO groups (id, name, published, description, image)
VALUES
  ("768040b3-7c05-4146-b11e-55229675d382",  'Kohi', true, '',''),
  ("50e0f008-9e08-4a1e-a8eb-3dc10cda360d", 'P8', true, '', ''),
  ("0cbb44e8-6a62-4ada-8ca0-5a2780f66312", 'Cola Taxi Okay', true, '', ''),
  ("c3b4dc8e-6350-43f8-b50f-75f82649f354", 'QueerKAstle', true, '', ''),
  ("ad4dd0f6-313e-4a4c-ba3b-4a41c7fc473f", 'Kinemathek', true, '', '')
ON CONFLICT DO NOTHING;

INSERT INTO places (id, name, published)
VALUES
  ("a9d73764-caf4-406d-8ec9-63635ed3a707",  'Kohi', true),
  ("49dcab2a-afff-4c2e-a2f1-ab7f6bb6a099", 'P8', true),
  ("e3a6074e-14ea-4e3c-8416-252fd42a9ea4", 'Cola Taxi Okay', true),
  ("05f7d306-b6ed-4103-9a41-1f5802e2f653", 'QueerKAstle', true),
  ("db59cde2-d31a-46ae-a75f-6e1760e51847", 'Kinemathek', true)
ON CONFLICT DO NOTHING;

INSERT INTO category (id, name, headline, description)
VALUES
    ("2a531521-817a-4d3b-a853-ca4bc254b1c3", "BAR_CAFE", "", ""),
    ("b67ac3fd-cf71-467c-814f-3d5588fb5a27", "BERATUNG", "", ""),
    ("67cb734c-442a-4fcf-9dc7-22dc0a8fcf26", "DIY", "", ""),
    ("a844abaf-fc6b-4097-819e-a0d96e40875f", "DEMO_KUNDGEBUNG", "", ""),
    ("98070939-a7ad-475d-a555-e5002504458f", "DISKUSSION", "", ""),
    ("d5795597-271f-4ab1-afd2-ec8b01128517", "FILM", "", ""),
    ("d5afeef9-1a5c-459c-bbf3-802a3ae8c5fc", "KONZERT", "", ""),
    ("a6ff52cd-d8a6-4679-bbaf-b8b068f01f88", "PARTY", "", ""),
    ("edabfcdc-b5bb-4f71-a26d-64339ebbe87c", "SONSTIGES", "", ""),
    ("716f6ac1-5754-49be-bf9d-3cb206e22488", "TREFFEN", "", ""),
    ("d96685b7-5b01-49b6-a15c-b9e394a6ed5a", "VORTRAG", "", ""),
    ("e8d49f15-33ab-4a6b-9386-f17edbe22d9c", "WORKSHOP", "", "")
ON CONFLICT DO NOTHING;

INSERT INTO topic (id, name, headline, description)
VALUES
    ("e5cb34c9-9483-4c54-9960-2ed320b851fa", "ANARCHISMUS", "", ""),
    ("0ba014f5-3982-4e0e-aee9-41dcb720f520", "ANTIFASCHISMUS", "", ""),
    ("f106e2a8-7f33-46a1-86d4-ee59cc8591be", "ANTIRASSISMUS", "", ""),
    ("9bf47f2b-b732-4456-b15b-a089768f3b64", "ANTISEMITISMUS", "", ""),
    ("c505df1b-e07d-4abc-8f62-c57e41e7e5fe", "ARBEITSKAMPF", "", ""),
    ("8c53b6b6-47a3-458d-9ea7-68be4ba35edd", "DIY", "", ""),
    ("1ffb2643-f483-40da-bdd9-c87fa782f925", "INTERNATIONALISMUS", "", ""),
    ("5d756edc-e2d0-4242-bd71-590c969d804c", "KLIMAGERECHTIGKEIT", "", ""),
    ("9eef33d7-6244-4c71-8961-6c54526d35a9", "KULTUR", "", ""),
    ("cad5594a-a9e8-4fbc-8cfd-75782853d060", "MOBILITAET", "", ""),
    ("c616cc5f-32bd-41fc-b90a-353de9e79733", "QUEERFEMINISMUS", "", ""),
    ("339d1d5b-17a9-4868-b5a2-c35a6a62b04d", "REFUGEE_RIGHTS", "", ""),
    ("3bccf0da-4c6d-47de-8668-1243c1973d3f", "REPRESSION", "", ""),
    ("b37939af-4c89-4b31-8fc2-8c0da5f2d948", "SOLIDARITAET", "", ""),
    ("16b417bd-2e9a-469e-9fe9-81e296c5c8df", "SONSTIGES", "", ""),
    ("cb90a4e1-4f71-40cd-9ca0-220d02911307", "SOZIALISMUS", "", ""),
    ("3071369a-7ad9-43be-a2ff-942c816c2a37", "TIERRECHTE", "", ""),
    ("93ecdc90-1099-4acb-bb34-e87912d71161", "OEKOLOGIE", "", "")
ON CONFLICT DO NOTHING;

INSERT INTO users (id, email, nickname, password)
VALUES
    ("be9638f8-22f9-463a-b223-d1da83e2fa89", "kohi@example.com","KOHI", "$2a$10$GEGjR6DcT.sXNim./OV8AOLwshbgPZ8QNNB89vXOfK6Me4NyO5ZOy"),
    ("9c9951f1-60c8-4e5c-9be9-fb7d0e59bf78", "p8@example.com","P8", "$2a$10$GEGjR6DcT.sXNim./OV8AOLwshbgPZ8QNNB89vXOfK6Me4NyO5ZOy"),
    ("574e37d0-381d-4629-96d2-af7ee19f330f", "karlsunruh-importer@example.com","karlsunruh-importer", "$2a$10$GEGjR6DcT.sXNim./OV8AOLwshbgPZ8QNNB89vXOfK6Me4NyO5ZOy"),
    ("134f4d14-86fb-4a27-9bc7-79ef9be58ec1", "hello@colataxiokay.com","ColaTaxiOkay", "$2a$10$GEGjR6DcT.sXNim./OV8AOLwshbgPZ8QNNB89vXOfK6Me4NyO5ZOy"),
    ("c8853207-c310-46c2-a326-5b0b6b2fe8ef", "info@queerkastle.de","QueerKAstle", "$2a$10$GEGjR6DcT.sXNim./OV8AOLwshbgPZ8QNNB89vXOfK6Me4NyO5ZOy"),
    ("bd4c503f-0554-4227-b7b2-a1817e02e0d9", "info@kinemathek-karslsruhe.de","QueerKAstle", "$2a$10$GEGjR6DcT.sXNim./OV8AOLwshbgPZ8QNNB89vXOfK6Me4NyO5ZOy")
ON CONFLICT DO NOTHING;

INSERT INTO groups_owned_by (group_id, user_id)
VALUES
    ("768040b3-7c05-4146-b11e-55229675d382","be9638f8-22f9-463a-b223-d1da83e2fa89"),
    ("50e0f008-9e08-4a1e-a8eb-3dc10cda360d", "9c9951f1-60c8-4e5c-9be9-fb7d0e59bf78"),
    ("0cbb44e8-6a62-4ada-8ca0-5a2780f66312", "134f4d14-86fb-4a27-9bc7-79ef9be58ec1"),
    ("c3b4dc8e-6350-43f8-b50f-75f82649f354", "c8853207-c310-46c2-a326-5b0b6b2fe8ef"),
    ("ad4dd0f6-313e-4a4c-ba3b-4a41c7fc473f", "bd4c503f-0554-4227-b7b2-a1817e02e0d9")
ON CONFLICT DO NOTHING;

INSERT INTO places_owned_by (place_id, user_id)
VALUES
    ("a9d73764-caf4-406d-8ec9-63635ed3a707","be9638f8-22f9-463a-b223-d1da83e2fa89"),
    ("49dcab2a-afff-4c2e-a2f1-ab7f6bb6a099", "9c9951f1-60c8-4e5c-9be9-fb7d0e59bf78"),
    ("e3a6074e-14ea-4e3c-8416-252fd42a9ea4", "134f4d14-86fb-4a27-9bc7-79ef9be58ec1"),
    ("05f7d306-b6ed-4103-9a41-1f5802e2f653", "c8853207-c310-46c2-a326-5b0b6b2fe8ef"),
    ("db59cde2-d31a-46ae-a75f-6e1760e51847", "bd4c503f-0554-4227-b7b2-a1817e02e0d9")
ON CONFLICT DO NOTHING;

