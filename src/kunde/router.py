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
from sqlalchemy.orm.exc import StaleDataError

from kunde.repository import KundeRepository
from kunde.schemas import KundeInput, KundeModel, KundeUpdate

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


@router.put("/{kunde_id}", status_code=status.HTTP_204_NO_CONTENT)
def put(
    kunde_id: int,
    kunde_update: KundeUpdate,
    repo: Annotated[KundeRepository, Depends()],
    if_match: Annotated[str | None, Header()] = None,
) -> Response:
    """Einen Kunden aktualisieren; Lost Updates werden durch `If-Match` vermieden."""
    if if_match is None:
        raise HTTPException(
            status.HTTP_428_PRECONDITION_REQUIRED, "Header If-Match fehlt"
        )

    kunde = repo.find_by_id(kunde_id)
    if kunde is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Kein Kunde mit ID {kunde_id}")
    if if_match != f'"{kunde.version}"':
        raise HTTPException(
            status.HTTP_412_PRECONDITION_FAILED,
            f"Die Version {if_match} ist nicht aktuell",
        )
    if any(k.id != kunde_id for k in repo.find(email=kunde_update.email)):
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            f"Die Email {kunde_update.email} existiert bereits",
        )

    kunde_update.update_entity(kunde)
    try:
        kunde = repo.update(kunde)
    except StaleDataError as err:
        # zwischen Lesen und Schreiben durch einen anderen Request geändert
        raise HTTPException(
            status.HTTP_412_PRECONDITION_FAILED,
            "Der Kunde wurde zwischenzeitlich geändert",
        ) from err
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
        headers={"ETag": f'"{kunde.version}"'},
    )
