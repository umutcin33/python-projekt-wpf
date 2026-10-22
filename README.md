# Python-Projekt

Wahlpflichtfach "KI-gestützte Serverentwicklung" – Umut Ulaş Cin

## Datenbank

PostgreSQL 18 und pgAdmin als Docker Container:

```sh
docker compose up -d
```

- PostgreSQL: `localhost:5433`, DB/User `projekt`, Passwort `p`
- pgAdmin: <http://localhost:8888>

Schema (`db/init`):

- `kunde` 1:1 `adresse`
- `kunde` 1:N `bestellung`

Neu initialisieren: `docker compose down -v` und danach `docker compose up -d`.
