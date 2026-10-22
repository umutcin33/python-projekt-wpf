"""Konfiguration über Umgebungsvariable."""

import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://projekt:p@localhost:5433/projekt",
)
