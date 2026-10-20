"""Minimal client for the Morningstar API on RapidAPI.

Set RAPIDAPI_KEY in your environment (or in a .env file at the repo root).
"""

import os

import requests

HOST = "morningstar13.p.rapidapi.com"


def _load_dotenv():
    """Read RAPIDAPI_KEY from a .env in the current folder or the repo root, if present."""
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
    for path in (".env", os.path.join(root, ".env")):
        if os.path.exists(path):
            for line in open(path, encoding="utf-8"):
                key, sep, value = line.strip().partition("=")
                if sep and value and not key.startswith("#"):
                    os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()


def get(path, **params):
    """GET an endpoint and return the parsed JSON."""
    key = os.environ.get("RAPIDAPI_KEY")
    if not key:
        raise SystemExit("Set RAPIDAPI_KEY first (see .env.example).")
    response = requests.get(
        f"https://{HOST}{path}",
        params={k: v for k, v in params.items() if v is not None},
        headers={"x-rapidapi-host": HOST, "x-rapidapi-key": key},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def component(details, name):
    """Payload of one /stock/details section, or None when that section did not load.

    Each section carries its own status. Some (companyReport, priceToFairValueSummary)
    come back with status 401 because they are Morningstar premium content.
    """
    section = (details.get("components") or {}).get(name) or {}
    return section.get("payload") if section.get("status") == 200 else None


def value(point):
    """The value of a data point, or None when it is missing or locked.

    Locked points (premium fields such as star ratings) carry a placeholder value
    that is not the real figure, so never use them.
    """
    if not point or point.get("locked"):
        return None
    return point.get("value")


def fmt(point):
    """A data point as display text: percent units get a % sign."""
    v = value(point)
    if v is None:
        return "-"
    if isinstance(v, (int, float)):
        text = f"{v:,}" if isinstance(v, int) else f"{v:,.2f}"
        return text + "%" if point.get("unit") == "percent" else text
    return str(v)
