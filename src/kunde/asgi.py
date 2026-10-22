"""FastAPI-Applikation."""

from fastapi import FastAPI

app = FastAPI(title="Kunde", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    """Prüfen, ob der Appserver läuft."""
    return {"status": "up"}
