"""Structured logging setup shared by app and tests."""
import logging
import sys


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=level.upper(),
        stream=sys.stdout,
        format="%(asctime)s %(levelname)s %(name)s :: %(message)s",
        force=True,
    )
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
