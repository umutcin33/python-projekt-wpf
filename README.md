# Python-Projekt: Kunde

Wahlpflichtfach "KI-gestützte Serverentwicklung" – Umut Ulaş Cin (92910)

REST-Appserver für Kunden mit FastAPI, Pydantic und SQLAlchemy auf PostgreSQL.

## Inhalt

- [Domain](#domain)
- [Voraussetzungen](#voraussetzungen)
- [Datenbank](#datenbank)
- [Appserver](#appserver)
- [REST-Schnittstelle](#rest-schnittstelle)
- [Tests](#tests)
- [Codequalität](#codequalität)
- [Projektstruktur](#projektstruktur)

## Domain

```text
┌──────────┐ 1     1 ┌──────────┐
│  kunde   │─────────│ adresse  │   1:1  (adresse.kunde_id UNIQUE)
│          │         └──────────┘
│          │ 1     N ┌────────────┐
│          │─────────│ bestellung │ 1:N  (bestellung.kunde_id)
└──────────┘         └────────────┘
```

- `kunde`: Name, Email (eindeutig), Geburtsdatum und `version` für optimistische Synchronisation
- `adresse`: genau eine Adresse je Kunde
- `bestellung`: beliebig viele Bestellungen je Kunde

## Voraussetzungen

- Git
- Docker Desktop mit Docker Compose
- Python 3.14 und [uv](https://docs.astral.sh/uv)

## Datenbank

PostgreSQL 18 und pgAdmin als Docker Container:

```sh
docker compose up -d
```

- PostgreSQL: `localhost:5433`, DB/User `projekt`, Passwort `p`
- pgAdmin (DB-Browser): <http://localhost:8888>

Beim ersten Start werden die Skripte in `db/init` ausgeführt:

| Skript | Inhalt |
| --- | --- |
| `01-schema.sql` | Tabellen `kunde`, `adresse` (1:1), `bestellung` (1:N) |
| `02-data.sql` | Testdaten: 3 Kunden mit Adresse und 4 Bestellungen |

Neu initialisieren: `docker compose down -v` und danach `docker compose up -d`.

## Appserver

```sh
uv sync
uv run kunde
```

- REST-Schnittstelle: <http://localhost:8000/kunden>
- OpenAPI-Dokumentation: <http://localhost:8000/docs>
- Health: <http://localhost:8000/health>

Die DB-URL kann über die Umgebungsvariable `DATABASE_URL` überschrieben werden.

## REST-Schnittstelle

| Request | Beschreibung | Statuscodes |
| --- | --- | --- |
| `GET /kunden/{id}` | Kunde mit Adresse und Bestellungen, Response mit `ETag` | 200, 404 |
| `GET /kunden/{id}` mit `If-None-Match` | Bedingter GET | 304 bei unveränderter Version |
| `GET /kunden?nachname=…&email=…` | Suche mit Query-Parametern | 200 |
| `POST /kunden` | Neuer Kunde, Validierung durch Pydantic | 201 mit `Location` und `ETag`, 409, 422 |
| `PUT /kunden/{id}` mit `If-Match` | Aktualisierung ohne Lost Updates | 204 mit neuem `ETag`, 404, 409, 412, 422, 428 |

Beispiele:

```sh
curl http://localhost:8000/kunden/1
curl -H 'If-None-Match: "0"' http://localhost:8000/kunden/1
curl "http://localhost:8000/kunden?nachname=muster"
```

### Vermeidung von Lost Updates

1. `GET /kunden/1` liefert den Header `ETag: "0"`.
2. `PUT /kunden/1` mit `If-Match: "0"` ist erfolgreich und liefert `ETag: "1"`.
3. Ein weiterer `PUT` mit dem veralteten `If-Match: "0"` wird mit `412 Precondition Failed`
   abgewiesen.

Zusätzlich prüft SQLAlchemy beim `UPDATE ... WHERE version = <alte Version>` die
Versionsnummer (`version_id_col`), so dass auch gleichzeitige Requests erkannt werden.

## Tests

Integrationstests mit pytest für GET und POST; die DB muss laufen:

```sh
docker compose up -d
uv run pytest
```

## Codequalität

```sh
uv run ruff check     # Linter
uv run ruff format    # Formatter
uv run ty check       # Type Checker
```

Die Konfiguration befindet sich in `pyproject.toml`.

## Projektstruktur

```text
src/kunde/
├── __init__.py    # main(): Start von uvicorn
├── asgi.py        # FastAPI-Applikation
├── config.py      # Konfiguration (DATABASE_URL)
├── db.py          # Engine und Session je Request (Dependency Injection)
├── entity.py      # SQLAlchemy-Entities Kunde, Adresse, Bestellung
├── schemas.py     # Pydantic-Modelle für Requests und Responses
├── repository.py  # DB-Zugriff
└── router.py      # REST-Endpoints
tests/
├── conftest.py    # Fixtures
├── test_get.py
└── test_post.py
```
