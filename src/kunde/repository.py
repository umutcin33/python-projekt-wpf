"""Repository für den DB-Zugriff auf Kunden."""

from collections.abc import Sequence
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
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

    def find(
        self, nachname: str | None = None, email: str | None = None
    ) -> Sequence[Kunde]:
        """Kunden zu optionalen Suchkriterien suchen."""
        statement = select(Kunde).order_by(Kunde.id)
        if nachname is not None:
            statement = statement.where(Kunde.nachname.ilike(f"%{nachname}%"))
        if email is not None:
            statement = statement.where(Kunde.email == email)
        return self.session.scalars(statement).all()

    def insert(self, kunde: Kunde) -> Kunde:
        """Einen neuen Kunden einschließlich Adresse und Bestellungen speichern."""
        self.session.add(kunde)
        self.session.commit()
        self.session.refresh(kunde)
        return kunde

    def update(self, kunde: Kunde) -> Kunde:
        """Änderungen an einem gelesenen Kunden speichern.

        Raises:
            StaleDataError: Der Kunde wurde zwischenzeitlich geändert.
        """
        kunde.version += 1
        self.session.commit()
        self.session.refresh(kunde)
        return kunde
