"""Entity-Klassen für SQLAlchemy."""

from datetime import date, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Basisklasse für alle Entity-Klassen."""


class Kunde(Base):
    """Kunde mit 1:1 Adresse und 1:N Bestellungen."""

    __tablename__ = "kunde"

    id: Mapped[int] = mapped_column(primary_key=True)
    version: Mapped[int] = mapped_column(default=0)
    nachname: Mapped[str]
    vorname: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    geburtsdatum: Mapped[date | None]
    erzeugt: Mapped[datetime] = mapped_column(server_default=func.now())
    aktualisiert: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    adresse: Mapped[Adresse] = relationship(
        back_populates="kunde", cascade="all, delete-orphan"
    )
    bestellungen: Mapped[list[Bestellung]] = relationship(
        back_populates="kunde", cascade="all, delete-orphan"
    )

    # Optimistische Synchronisation: UPDATE ... WHERE version = <alte Version>
    # Die Version wird im Repository hochgezählt, damit auch eine geänderte
    # Adresse als Änderung des Kunden zählt.
    __mapper_args__: dict[str, Any] = {  # noqa: RUF012
        "version_id_col": version,
        "version_id_generator": False,
    }


class Adresse(Base):
    """Adresse eines Kunden (1:1)."""

    __tablename__ = "adresse"

    id: Mapped[int] = mapped_column(primary_key=True)
    strasse: Mapped[str]
    hausnummer: Mapped[str]
    plz: Mapped[str]
    ort: Mapped[str]
    kunde_id: Mapped[int] = mapped_column(ForeignKey("kunde.id"), unique=True)

    kunde: Mapped[Kunde] = relationship(back_populates="adresse")


class Bestellung(Base):
    """Bestellung eines Kunden (1:N)."""

    __tablename__ = "bestellung"

    id: Mapped[int] = mapped_column(primary_key=True)
    produktname: Mapped[str]
    menge: Mapped[int]
    preis: Mapped[Decimal]
    bestelldatum: Mapped[date] = mapped_column(server_default=func.current_date())
    kunde_id: Mapped[int] = mapped_column(ForeignKey("kunde.id"))

    kunde: Mapped[Kunde] = relationship(back_populates="bestellungen")
