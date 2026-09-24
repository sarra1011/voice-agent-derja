"""Loads .env if python-dotenv is installed; everything else reads os.environ."""
import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # pragma: no cover
    pass


def env(name: str, default: str | None = None) -> str | None:
    value = os.environ.get(name)
    return value if value else default
