"""REST-Schnittstelle für Kunden."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from kunde.repository import KundeRepository
from kunde.schemas import KundeModel

router = APIRouter(prefix="/kunden", tags=["Kunde"])


@router.get("/{kunde_id}")
def get_by_id(
    kunde_id: int,
    repo: Annotated[KundeRepository, Depends()],
) -> KundeModel:
    """Einen Kunden zur ID lesen."""
    kunde = repo.find_by_id(kunde_id)
    if kunde is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Kein Kunde mit ID {kunde_id}")
    return KundeModel.model_validate(kunde)
