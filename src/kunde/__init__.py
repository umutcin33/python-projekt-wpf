"""REST-Appserver für Kunden."""

import uvicorn


def main() -> None:
    """Einstiegspunkt für `uv run kunde`."""
    uvicorn.run("kunde.asgi:app", host="127.0.0.1", port=8000, reload=True)
