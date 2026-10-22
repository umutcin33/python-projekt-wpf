"""Integrationstests für GET-Requests."""

from fastapi import status
from fastapi.testclient import TestClient


def test_get_by_id(client: TestClient) -> None:
    response = client.get("/kunden/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.headers["ETag"] == '"0"'
    body = response.json()
    assert body["id"] == 1
    assert body["nachname"] == "Mustermann"
    assert body["adresse"]["ort"] == "Karlsruhe"
    assert len(body["bestellungen"]) == 2  # noqa: PLR2004


def test_get_by_id_nicht_vorhanden(client: TestClient) -> None:
    response = client.get("/kunden/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_by_id_ungueltige_id(client: TestClient) -> None:
    response = client.get("/kunden/abc")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_get_by_id_if_none_match_aktuell(client: TestClient) -> None:
    response = client.get("/kunden/1", headers={"If-None-Match": '"0"'})

    assert response.status_code == status.HTTP_304_NOT_MODIFIED
    assert not response.content


def test_get_by_id_if_none_match_veraltet(client: TestClient) -> None:
    response = client.get("/kunden/1", headers={"If-None-Match": '"99"'})

    assert response.status_code == status.HTTP_200_OK


def test_get_nachname(client: TestClient) -> None:
    response = client.get("/kunden", params={"nachname": "muster"})

    assert response.status_code == status.HTTP_200_OK
    nachnamen = [kunde["nachname"] for kunde in response.json()]
    assert nachnamen
    assert all("muster" in nachname.lower() for nachname in nachnamen)


def test_get_email(client: TestClient) -> None:
    response = client.get("/kunden", params={"email": "anna@acme.de"})

    assert response.status_code == status.HTTP_200_OK
    assert [kunde["id"] for kunde in response.json()] == [3]


def test_get_nachname_nicht_vorhanden(client: TestClient) -> None:
    response = client.get("/kunden", params={"nachname": "gibtsnicht"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
