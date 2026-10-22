"""REST-Schnittstelle für Kunden."""

from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Header,
    HTTPException,
    Query,
    Request,
    Response,
    status,
)

from kunde.repository import KundeRepository
from kunde.schemas import KundeInput, KundeModel

router = APIRouter(prefix="/kunden", tags=["Kunde"])


@router.get("")
def get(
    repo: Annotated[KundeRepository, Depends()],
    nachname: Annotated[str | None, Query(min_length=1)] = None,
    email: Annotated[str | None, Query(min_length=3)] = None,
) -> list[KundeModel]:
    """Kunden mit Query-Parametern suchen, z.B. `/kunden?nachname=Muster`."""
    kunden = repo.find(nachname=nachname, email=email)
    return [KundeModel.model_validate(kunde) for kunde in kunden]


@router.get("/{kunde_id}", response_model=KundeModel)
def get_by_id(
    kunde_id: int,
    repo: Annotated[KundeRepository, Depends()],
    response: Response,
    if_none_match: Annotated[str | None, Header()] = None,
) -> KundeModel | Response:
    """Einen Kunden zur ID lesen, bedingt durch `If-None-Match`."""
    kunde = repo.find_by_id(kunde_id)
    if kunde is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Kein Kunde mit ID {kunde_id}")

    etag = f'"{kunde.version}"'
    if if_none_match == etag:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED)
    response.headers["ETag"] = etag
    return KundeModel.model_validate(kunde)


@router.post("", status_code=status.HTTP_201_CREATED)
def post(
    kunde_input: KundeInput,
    repo: Annotated[KundeRepository, Depends()],
    request: Request,
    response: Response,
) -> KundeModel:
    """Einen neuen Kunden anlegen; der Request-Body wird durch Pydantic validiert."""
    if repo.find(email=kunde_input.email):
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            f"Die Email {kunde_input.email} existiert bereits",
        )

    kunde = repo.insert(kunde_input.to_entity())
    response.headers["Location"] = str(request.url_for("get_by_id", kunde_id=kunde.id))
    response.headers["ETag"] = f'"{kunde.version}"'
    return KundeModel.model_validate(kunde)
