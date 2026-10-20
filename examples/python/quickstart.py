"""Look up a stock by ticker and exchange, then read its real-time quote.

    python quickstart.py AAPL xnas
    python quickstart.py MSFT xnas

/stock/details returns the performanceID that every /stock/... research endpoint takes.
"""

import sys

from client import component, fmt, get

ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
exchange = sys.argv[2] if len(sys.argv) > 2 else "xnas"

# 1. The overview page: identifiers, profile, key statistics.
details = get("/stock/details", ticker=ticker, exchange=exchange)
page = details["page"]
print(f"{page['name']} ({page['exchange']}:{page['ticker']})  performanceID {page['performanceID']}")

profile = component(details, "profile") or {}
for key in ("sector", "industry", "stockStyleBox", "totalEmployees"):
    point = (profile.get("dataPoints") or {}).get(key)
    if point:
        print(f"  {point['name']:<28} {fmt(point)}")

stats = (component(details, "keyStatistics") or {}).get("dataPoints") or {}
for point in stats.values():
    if isinstance(point.get("value"), (int, float)):
        print(f"  {point['name']:<28} {fmt(point)}")

# 2. The real-time quote. The response is keyed by performanceID, and every field is an
#    object with its value plus the trade date, currency and exchange it came from.
quotes = get("/stock/real-time", performanceId=page["performanceID"])
quote = quotes.get(page["performanceID"]) or next(iter(quotes.values()))
print("\nReal-time quote:")
for key in ("lastPrice", "netChange", "percentNetChange", "previousClosePrice", "volume",
            "yearHighPrice", "yearLowPrice", "marketCap", "tradingStatus"):
    field = quote.get(key) or {}
    where = (field.get("exchange") or {}).get("value", "")
    when = (field.get("date") or {}).get("value", "")
    print(f"  {key:<20} {field.get('value')!s:<20} {where:<5} {when}")
