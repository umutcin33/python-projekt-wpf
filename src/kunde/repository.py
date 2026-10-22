"""Repository für den DB-Zugriff auf Kunden."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from kunde.db import get_session
from kunde.entity import Kunde


class KundeRepository:
    """Lesen und Schreiben von Kunden."""

    def __init__(self, session: Annotated[Session, Depends(get_session)]) -> None:
        """Session wird durch Dependency Injection übergeben."""
        self.session = session

    def find_by_id(self, kunde_id: int) -> Kunde | None:
        """Einen Kunden zur ID suchen."""
        return self.session.get(Kunde, kunde_id)
