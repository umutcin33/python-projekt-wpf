"""Pydantic-Modelle für Requests und Responses."""

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class AdresseModel(BaseModel):
    """Adresse in einer Response."""

    model_config = ConfigDict(from_attributes=True)

    strasse: str
    hausnummer: str
    plz: str
    ort: str


class BestellungModel(BaseModel):
    """Bestellung in einer Response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    produktname: str
    menge: int
    preis: Decimal
    bestelldatum: date


class KundeModel(BaseModel):
    """Kunde in einer Response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    nachname: str
    vorname: str
    email: str
    geburtsdatum: date | None
    adresse: AdresseModel
    bestellungen: list[BestellungModel]
