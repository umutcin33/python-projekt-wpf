"""Pydantic-Modelle für Requests und Responses."""

from datetime import date
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, PastDate

from kunde.entity import Adresse, Bestellung, Kunde

Name = Annotated[str, Field(min_length=1, max_length=64)]


class AdresseInput(BaseModel):
    """Adresse in einem POST- oder PUT-Request."""

    strasse: Annotated[str, Field(min_length=1, max_length=128)]
    hausnummer: Annotated[str, Field(min_length=1, max_length=16)]
    plz: Annotated[str, Field(pattern=r"^\d{5}$")]
    ort: Name

    def to_entity(self) -> Adresse:
        """Entity-Objekt erzeugen."""
        return Adresse(**self.model_dump())


class BestellungInput(BaseModel):
    """Bestellung in einem POST-Request."""

    produktname: Annotated[str, Field(min_length=1, max_length=128)]
    menge: Annotated[int, Field(gt=0)]
    preis: Annotated[Decimal, Field(ge=0, max_digits=10, decimal_places=2)]

    def to_entity(self) -> Bestellung:
        """Entity-Objekt erzeugen."""
        return Bestellung(**self.model_dump())


class KundeUpdate(BaseModel):
    """Kunde in einem PUT-Request, d.h. ohne Bestellungen."""

    nachname: Name
    vorname: Name
    email: EmailStr
    geburtsdatum: PastDate | None = None
    adresse: AdresseInput

    def update_entity(self, kunde: Kunde) -> None:
        """Ein vorhandenes Entity-Objekt mit den neuen Werten überschreiben."""
        kunde.nachname = self.nachname
        kunde.vorname = self.vorname
        kunde.email = self.email
        kunde.geburtsdatum = self.geburtsdatum
        for key, value in self.adresse.model_dump().items():
            setattr(kunde.adresse, key, value)


class KundeInput(KundeUpdate):
    """Kunde in einem POST-Request."""

    bestellungen: list[BestellungInput] = []

    def to_entity(self) -> Kunde:
        """Entity-Objekt einschließlich Adresse und Bestellungen erzeugen."""
        return Kunde(
            nachname=self.nachname,
            vorname=self.vorname,
            email=self.email,
            geburtsdatum=self.geburtsdatum,
            adresse=self.adresse.to_entity(),
            bestellungen=[b.to_entity() for b in self.bestellungen],
        )


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
