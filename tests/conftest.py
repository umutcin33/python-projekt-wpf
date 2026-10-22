"""Fixtures für die Integrationstests mit der laufenden DB."""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete

from kunde.asgi import app
from kunde.db import engine
from kunde.entity import Kunde

NEUE_EMAIL = "pytest@acme.de"


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def neue_email() -> Iterator[str]:
    """Email für einen neuen Kunden; der Kunde wird nach dem Test gelöscht."""
    yield NEUE_EMAIL
    with engine.begin() as connection:
        connection.execute(delete(Kunde).where(Kunde.email == NEUE_EMAIL))
