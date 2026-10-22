"""FastAPI-Applikation."""

from fastapi import FastAPI

from kunde.router import router

app = FastAPI(title="Kunde", version="0.1.0")
app.include_router(router)


@app.get("/health")
def health() -> dict[str, str]:
    """Prüfen, ob der Appserver läuft."""
    return {"status": "up"}
