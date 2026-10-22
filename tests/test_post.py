"""Integrationstests für POST-Requests."""

from typing import Any

from fastapi import status
from fastapi.testclient import TestClient


def neuer_kunde(email: str) -> dict[str, Any]:
    return {
        "nachname": "Test",
        "vorname": "Tina",
        "email": email,
        "geburtsdatum": "1999-05-05",
        "adresse": {
            "strasse": "Testweg",
            "hausnummer": "1",
            "plz": "76131",
            "ort": "Karlsruhe",
        },
        "bestellungen": [{"produktname": "Buch", "menge": 2, "preis": "12.50"}],
    }


def test_post(client: TestClient, neue_email: str) -> None:
    response = client.post("/kunden", json=neuer_kunde(neue_email))

    assert response.status_code == status.HTTP_201_CREATED
    assert response.headers["ETag"] == '"0"'
    body = response.json()
    assert body["email"] == neue_email
    assert body["adresse"]["plz"] == "76131"
    assert body["bestellungen"][0]["produktname"] == "Buch"

    # der neue Kunde ist über den Location-Header lesbar
    location = response.headers["Location"]
    assert location.endswith(f"/kunden/{body['id']}")
    assert client.get(location).json() == body


def test_post_email_existiert(client: TestClient) -> None:
    response = client.post("/kunden", json=neuer_kunde("max@acme.de"))

    assert response.status_code == status.HTTP_409_CONFLICT


def test_post_ungueltig(client: TestClient, neue_email: str) -> None:
    kunde = neuer_kunde(neue_email)
    kunde["nachname"] = ""
    kunde["email"] = "keine-email"
    kunde["geburtsdatum"] = "2999-01-01"
    kunde["adresse"]["plz"] = "123"
    kunde["bestellungen"][0]["menge"] = 0

    response = client.post("/kunden", json=kunde)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    fehler = {".".join(map(str, e["loc"][1:])) for e in response.json()["detail"]}
    assert fehler == {
        "nachname",
        "email",
        "geburtsdatum",
        "adresse.plz",
        "bestellungen.0.menge",
    }
