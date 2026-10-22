"""DB-Zugriff mit SQLAlchemy."""

from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from kunde.config import DATABASE_URL

engine = create_engine(DATABASE_URL)


def get_session() -> Iterator[Session]:
    """Session je Request für Dependency Injection bereitstellen."""
    with Session(engine) as session:
        yield session
