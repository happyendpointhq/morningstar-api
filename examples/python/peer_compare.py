"""Compare a stock's valuation, profitability and balance sheet with its competitors.

    python peer_compare.py AAPL xnas

One /stock/details call. Its valuationVsBenchmarks, profitabilityVsBenchmarks and
financialStrengthVsBenchmarks sections hold the stock and the competitors Morningstar
lists for it, one row per ticker.
"""

import sys

from client import component, fmt, get

SECTIONS = {
    "valuationVsBenchmarks": "Valuation",
    "profitabilityVsBenchmarks": "Profitability",
    "financialStrengthVsBenchmarks": "Financial strength",
}


def main():
    ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    exchange = sys.argv[2] if len(sys.argv) > 2 else "xnas"
    details = get("/stock/details", ticker=ticker, exchange=exchange)
    names = {c["ticker"]: c["name"] for c in (component(details, "competitors") or {}).get("results", [])}
    names[details["page"]["ticker"]] = details["page"]["name"]

    for section, title in SECTIONS.items():
        rows = (component(details, section) or {}).get("dataPoints") or []
        if not rows:
            print(f"\n{title}: not available")
            continue
        metrics = list(rows[0]["values"])
        labels = [rows[0]["values"][m]["name"] for m in metrics]
        print(f"\n{title}")
        print(f"  {'':<30}" + "".join(f"{label[:26]:>28}" for label in labels))
        for row in rows:
            name = f"{row['label']} {names.get(row['label'], '')}"[:30]
            cells = "".join(f"{fmt(row['values'].get(m)):>28}" for m in metrics)
            print(f"  {name:<30}{cells}")


if __name__ == "__main__":
    main()
