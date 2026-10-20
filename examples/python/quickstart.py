"""Find a stock by name (or ticker and exchange), then read its overview and real-time quote.

    python quickstart.py apple
    python quickstart.py "coca cola"
    python quickstart.py MSFT xnas

/stock/details returns the performanceID that every /stock/... research endpoint takes.
"""

import sys

from client import component, fmt, get

if len(sys.argv) > 2:
    ticker, exchange = sys.argv[1], sys.argv[2]
else:
    # 0. Resolve a name with /auto-complete. Matches are ranked by score and mix in other
    #    companies ("apple" also returns Apple Hospitality REIT), so check what you got.
    query = sys.argv[1] if len(sys.argv) > 1 else "apple"
    matches = [e["value"] for e in get("/auto-complete", q=query).get("entities", [])
               if e.get("type") == "security"]
    if not matches:
        raise SystemExit(f"No Morningstar security matches {query!r}")
    for m in matches[:3]:
        print(f"  {m['exchange']}:{m['ticker']:<6} {m['name']}  ({m['investmentType']})")
    ticker = matches[0]["ticker"]
    # /auto-complete returns upper-case exchange codes; /stock/details takes lower case.
    exchange = matches[0]["exchange"].lower()
    print()

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
